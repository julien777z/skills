// Turn Roblox Studio's MCP server on or off from inside a macOS guest, without a viewer.
//
// Run in the guest's signed-in session, from a process the guest grants Accessibility
// (for example `osascript` over SSH on a Cirrus Labs image):
//
//   osascript -l JavaScript guest_studio_mcp.js <studio-pid> on|off|read
//
// It finds controls by their on-screen text and tooltips with Vision, so it does not depend
// on the display size or Studio's panel layout, clicks in screen points, and checks the
// screen after every click. It exits nonzero unless the status bar reaches the target state.
// `read` prints each recognized line with its center in screen points.

ObjC.import("AppKit");
ObjC.import("CoreGraphics");
ObjC.import("Vision");

const CAPTURE_PATH = "/tmp/guest-studio-mcp.png";
const ESCAPE_KEY_CODE = 53;

// Text recognition misreads small labels slightly, so prompts are matched by their start.
const ASK_PROMPT = /^Ask assist/i;

// A click is retried this many times while the screen has not changed, because a panel can
// take one click for focus before it acts.
const CLICK_ATTEMPTS = 4;

// Whole passes through the settings before the run reports failure.
const RUN_ATTEMPTS = 3;

// Rows of icons without text are searched in steps of this many points.
const PROBE_STEP = 8;

const systemEvents = Application("System Events");
const source = $.CGEventSourceCreate($.kCGEventSourceStateHIDSystemState);

function studioWindow(process) {
  return process.windows.whose({ name: { _contains: "Roblox Studio" } })[0];
}

// Studio can hold a stale window origin and register clicks below where they land on
// screen; setting the frame again makes it recompute.
function resetStudioWindow(process) {
  process.frontmost = true;

  const window = studioWindow(process);
  const [x, y] = window.position();
  const [width, height] = window.size();

  window.position = [x, y + 8];
  delay(0.4);
  window.position = [x, y];
  window.size = [width, height];
  delay(0.6);

  return { x, y, width, height, right: x + width };
}

function postMouse(type, x, y) {
  const event = $.CGEventCreateMouseEvent(source, type, $.CGPointMake(x, y), $.kCGMouseButtonLeft);

  // Studio's widgets ignore a press without a click count, and its web panels one without
  // pressure.
  $.CGEventSetIntegerValueField(event, $.kCGMouseEventClickState, 1);
  $.CGEventSetDoubleValueField(event, $.kCGMouseEventPressure, type === $.kCGEventLeftMouseDown ? 1 : 0);
  $.CGEventPost($.kCGHIDEventTap, event);
}

function hover(x, y) {
  for (const step of [12, 6, 0]) {
    postMouse($.kCGEventMouseMoved, x - step, y + step);
    delay(0.12);
  }
}

function click(x, y) {
  hover(x, y);
  postMouse($.kCGEventLeftMouseDown, x, y);
  delay(0.1);
  postMouse($.kCGEventLeftMouseUp, x, y);
}

function pressEscape() {
  for (const down of [true, false]) {
    $.CGEventPost($.kCGHIDEventTap, $.CGEventCreateKeyboardEvent(source, ESCAPE_KEY_CODE, down));
    delay(0.05);
  }

  delay(0.4);
}

// Returns recognized lines with their centers and right edges in screen points.
function readScreen() {
  const task = $.NSTask.launchedTaskWithLaunchPathArguments("/usr/sbin/screencapture", $(["-x", CAPTURE_PATH]));

  task.waitUntilExit;

  const screen = $.NSScreen.mainScreen.frame.size;
  const url = $.NSURL.fileURLWithPath(CAPTURE_PATH);
  const request = $.VNRecognizeTextRequest.alloc.init;

  // Vision skips text shorter than 1/32 of the image by default, which drops Studio's
  // small labels on a 1x display.
  request.minimumTextHeight = 0.004;

  const handler = $.VNImageRequestHandler.alloc.initWithURLOptions(url, $({}));

  handler.performRequestsError($([request]), null);

  const lines = [];
  const results = request.results;

  for (let index = 0; index < results.count; index++) {
    const observation = results.objectAtIndex(index);
    const box = observation.boundingBox;

    lines.push({
      text: observation.topCandidates(1).firstObject.string.js,
      x: (box.origin.x + box.size.width / 2) * screen.width,
      y: (1 - box.origin.y - box.size.height / 2) * screen.height,
      right: (box.origin.x + box.size.width) * screen.width,
    });
  }

  return lines;
}

function findLine(pattern, lines = readScreen()) {
  return lines.find((line) => pattern.test(line.text));
}

function waitFor(pattern, seconds) {
  const deadline = Date.now() + seconds * 1000;

  do {
    const line = findLine(pattern);

    if (line) {
      return line;
    }

    delay(0.5);
  } while (Date.now() < deadline);

  return null;
}

// Clicks until the expected text appears, checking the screen after each click.
function clickUntil(x, y, pattern) {
  for (let attempt = 0; attempt < CLICK_ATTEMPTS; attempt++) {
    click(x, y);

    // A web panel can take several seconds to draw; a retry too soon closes it again.
    const line = waitFor(pattern, 6);

    if (line) {
      return line;
    }
  }

  return null;
}

function mcpStatus() {
  const line = findLine(/MCP (Ready|off)/i);

  return line ? line.text.match(/MCP (Ready|off)/i)[0].toLowerCase() : "unknown";
}

// The Assistant toolbar button has no label, so it is found by its "AI Assistant" tooltip,
// searching right of the Collaborate button or, without one, leftward from the window edge.
// Text recognition can read a leading icon as a symbol and "AI" as "Al", so the patterns
// allow both.
function findAssistantButton(frame) {
  const toolbar = readScreen().filter((line) => line.y > frame.y && line.y < frame.y + 90);
  const collaborate = findLine(/Collaborate$/, toolbar);
  const y = collaborate ? collaborate.y : frame.y + 50;
  const start = collaborate ? collaborate.right + PROBE_STEP : frame.right - 40;
  const direction = collaborate ? 1 : -1;

  for (let offset = 0; offset <= 200; offset += PROBE_STEP) {
    const x = start + direction * offset;

    if (x < frame.x || x > frame.right) {
      break;
    }

    hover(x, y);

    if (waitFor(/^A[Il1] Assistant$/, 1.5)) {
      return { x, y };
    }
  }

  throw new Error("The AI Assistant toolbar button was not found");
}

function openAssistantPanel(frame) {
  const prompt = findLine(ASK_PROMPT);

  if (prompt) {
    return prompt;
  }

  // A tooltip left on screen keeps Studio's toolbar from taking clicks.
  hover(frame.x + frame.width / 2, frame.y + frame.height / 2);
  pressEscape();

  const button = findAssistantButton(frame);
  const opened = clickUntil(button.x, button.y, ASK_PROMPT);

  if (!opened) {
    throw new Error("The Assistant panel did not open");
  }

  return opened;
}

// The panel's menu button has no label either; it is the rightmost control on the panel's
// header row, so positions are tried from the window edge inward until its menu appears.
function openAssistantMenu(frame, prompt) {
  const lines = readScreen();
  const title = lines
    .filter((line) => /^Assistant$/i.test(line.text) && line.y < prompt.y)
    .sort((a, b) => b.y - a.y)[0];

  if (!title) {
    throw new Error("The Assistant panel title is not on screen");
  }

  // The menu button shares the row of the first label under the panel title.
  const headerRow = lines
    .filter((line) => line.y > title.y + 10 && line.y < title.y + 60 && line.x > title.x - 120)
    .sort((a, b) => a.y - b.y)[0];
  const headerY = headerRow ? headerRow.y : title.y + 35;

  // The panel is a web view that spends a click taking focus, and a click elsewhere takes
  // focus away, so every attempt first clicks its chat area, between the header and the
  // prompt; the prompt field itself can raise suggestions over the header.
  const focusY = (headerY + prompt.y) / 2;

  for (let x = frame.right - 12; x > title.x; x -= PROBE_STEP) {
    click(title.x, focusY);
    delay(0.8);
    click(x, headerY);

    const settings = waitFor(/^Settings$/i, 2);

    if (settings && findLine(/^Usage/i)) {
      return settings;
    }
  }

  throw new Error("The Assistant menu did not open");
}

function setMcpSwitch(process, frame, target) {
  const prompt = openAssistantPanel(frame);
  const settings = openAssistantMenu(frame, prompt);
  const page = clickUntil(settings.x, settings.y, /^MCP Servers$/i);

  if (!page) {
    throw new Error("Assistant Settings did not open");
  }

  const row = clickUntil(page.x, page.y, /^Enable/i);

  if (!row) {
    throw new Error("The MCP server switch is not on screen");
  }

  const dialog = process.windows.whose({ name: "Assistant Settings" })[0];
  const [dialogX] = dialog.position();
  const [dialogWidth] = dialog.size();

  // The switch sits at the right end of its row, inside the dialog's padding.
  for (let inset = 40; inset <= 90 && mcpStatus() !== target; inset += 6) {
    click(dialogX + dialogWidth - inset, row.y);
    delay(1.5);
  }

  closeAssistantSettings(process);
}

function closeAssistantSettings(process) {
  const dialogs = process.windows.whose({ name: "Assistant Settings" });

  if (dialogs.length > 0) {
    dialogs[0].buttons.whose({ subrole: "AXCloseButton" })[0].click();
    delay(1);
  }
}

function run(argv) {
  if (argv[1] === "read") {
    return readScreen().map((line) => `${Math.round(line.x)},${Math.round(line.y)} ${line.text}`).join("\n");
  }

  const pid = Number(argv[0]);
  const target = argv[1] === "off" ? "mcp off" : "mcp ready";
  const process = systemEvents.processes.whose({ unixId: pid })[0];

  if (mcpStatus() === target) {
    return `already ${target}`;
  }

  let failure = null;

  // Studio's web panels occasionally drop a click, so a failed pass starts over from a
  // closed dialog and a reset window.
  for (let attempt = 0; attempt < RUN_ATTEMPTS && mcpStatus() !== target; attempt++) {
    try {
      setMcpSwitch(process, resetStudioWindow(process), target);
    } catch (error) {
      failure = error;
      closeAssistantSettings(process);
      pressEscape();
    }
  }

  const status = mcpStatus();

  if (status !== target) {
    throw new Error(`Studio reports ${status}, expected ${target}${failure ? `; last step failed: ${failure.message}` : ""}`);
  }

  return status;
}
