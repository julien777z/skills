// Turn Roblox Studio's MCP server on or off from inside a macOS guest, without a viewer.
//
// Run in the guest's signed-in session over SSH:
//
//   osascript -l JavaScript guest_studio_mcp.js <studio-pid> on|off
//   osascript -l JavaScript guest_studio_mcp.js read
//
// JavaScript for Automation is used because `osascript` holds the guest's Accessibility grant on a
// Cirrus Labs image and reaches Vision and CoreGraphics without extra packages.
//
// It finds controls by their on-screen text and tooltips with Vision, clicks in screen points, and
// checks the screen after every click. It exits nonzero unless the status bar reaches the target
// state. `read` prints each recognized line with its center in screen points.

ObjC.import("AppKit");
ObjC.import("CoreGraphics");
ObjC.import("Foundation");
ObjC.import("Vision");

const CAPTURE_PATH = `${$.NSTemporaryDirectory().js}guest-studio-mcp.png`;
const ESCAPE_KEY_CODE = 53;

// Text recognition misreads small labels slightly, so labels are matched loosely: "AI" can
// come back as "Al", a leading icon as a symbol, and a prompt with a wrong final letter.
const ASK_PROMPT = /^Ask assist/i;
const ASSISTANT_TOOLTIP = /^A[Il1] Assistant$/;

// A label click is retried this many times until the text it should produce appears, because a
// panel can spend a click taking focus before it acts.
const CLICK_ATTEMPTS = 4;

// Whole passes through the settings before the run reports failure.
const RUN_ATTEMPTS = 3;

// Rows of icons without text are searched in steps of this many points.
const PROBE_STEP = 8;

// The Assistant panel's menu button sits within this many points right of the panel title at
// the panel's default width.
const PANEL_MENU_REACH = 140;

const systemEvents = Application("System Events");
const source = $.CGEventSourceCreate($.kCGEventSourceStateHIDSystemState);

function studioWindow(process) {
  return process.windows.whose({ name: { _contains: "Roblox Studio" } })[0];
}

function bounds(window) {
  const [x, y] = window.position();
  const [width, height] = window.size();

  return { x, y, width, height, right: x + width, bottom: y + height };
}

function contains(area, line) {
  return line.x > area.x && line.x < area.right && line.y > area.y && line.y < area.bottom;
}

// Studio can hold a stale window origin and register clicks below where they land on screen;
// setting the frame again makes it recompute.
function resetStudioWindow(process) {
  process.frontmost = true;

  const window = studioWindow(process);
  const frame = bounds(window);

  window.position = [frame.x, frame.y + 8];
  delay(0.4);
  window.position = [frame.x, frame.y];
  window.size = [frame.width, frame.height];
  delay(0.6);

  return frame;
}

function postMouse(type, x, y) {
  const event = $.CGEventCreateMouseEvent(source, type, $.CGPointMake(x, y), $.kCGMouseButtonLeft);

  const pressure = type === $.kCGEventLeftMouseDown ? 1 : 0;

  // Studio's widgets ignore a press without a click count, and its web panels one without
  // pressure.
  $.CGEventSetIntegerValueField(event, $.kCGMouseEventClickState, 1);
  $.CGEventSetDoubleValueField(event, $.kCGMouseEventPressure, pressure);
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
  const files = $.NSFileManager.defaultManager;

  files.removeItemAtPathError(CAPTURE_PATH, null);

  const task = $.NSTask.launchedTaskWithLaunchPathArguments(
    "/usr/sbin/screencapture",
    $(["-x", CAPTURE_PATH]),
  );

  task.waitUntilExit;

  if (task.terminationStatus !== 0 || !files.fileExistsAtPath(CAPTURE_PATH)) {
    throw new Error("Screen capture failed; the session needs Screen Recording access");
  }

  const screen = $.NSScreen.mainScreen.frame.size;
  const url = $.NSURL.fileURLWithPath(CAPTURE_PATH);
  const request = $.VNRecognizeTextRequest.alloc.init;

  // Vision skips text shorter than 1/32 of the image by default, which drops Studio's small
  // labels on a 1x display.
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

function waitFor(pattern, seconds, area = null) {
  const deadline = Date.now() + seconds * 1000;

  do {
    const line = readScreen().find(
      (candidate) => pattern.test(candidate.text) && (!area || contains(area, candidate)),
    );

    if (line) {
      return line;
    }

    delay(0.5);
  } while (Date.now() < deadline);

  return null;
}

// Clicks a label until the text it should produce appears. Before each retry the label is
// found again, so a retry never lands on whatever replaced it.
function clickLabelUntil(label, labelPattern, expected) {
  let target = label;

  for (let attempt = 0; attempt < CLICK_ATTEMPTS && target; attempt++) {
    click(target.x, target.y);

    // A web panel can take several seconds to draw; a retry too soon closes it again.
    const line = waitFor(expected, 6);

    if (line) {
      return line;
    }

    target = findLine(labelPattern);
  }

  return null;
}

function mcpStatus() {
  const line = findLine(/MCP (Ready|off)/i);

  return line ? line.text.match(/MCP (Ready|off)/i)[0].toLowerCase() : "unknown";
}

// The Assistant toolbar button has no label, so it is found by its "AI Assistant" tooltip next to
// the pointer, searching right of the Collaborate button or, without one, leftward from the
// window edge.
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

    const near = { x: x - 60, right: x + 260, y, bottom: y + 80 };

    if (waitFor(ASSISTANT_TOOLTIP, 1.5, near)) {
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

  for (let attempt = 0; attempt < CLICK_ATTEMPTS; attempt++) {
    click(button.x, button.y);

    const opened = waitFor(ASK_PROMPT, 6);

    if (opened) {
      return opened;
    }
  }

  throw new Error("The Assistant panel did not open");
}

// A point in the panel between its header and prompt with no text near it, so a focus click
// lands on empty chat area rather than a message or a suggestion.
function emptyPanelPoint(lines, title, headerY, prompt) {
  for (let y = headerY + 24; y < prompt.y - 24; y += 12) {
    const crowded = lines.some(
      (line) => Math.abs(line.y - y) < 12 && Math.abs(line.x - title.x) < 120,
    );

    if (!crowded) {
      return { x: title.x, y };
    }
  }

  return null;
}

// The panel's menu button has no label either; it is the rightmost control on the panel's
// header row, so positions inside the panel are tried from the right until its menu appears.
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
  const focus = emptyPanelPoint(lines, title, headerY, prompt);

  // The panel is a web view that spends a click taking focus, and a click elsewhere takes focus
  // away, so every attempt first clicks empty chat area.
  const scanStart = Math.min(frame.right - 12, title.x + PANEL_MENU_REACH);

  for (let x = scanStart; x > title.x; x -= PROBE_STEP) {
    if (focus) {
      click(focus.x, focus.y);
      delay(0.8);
    }

    click(x, headerY);

    const settings = waitFor(/^Settings$/i, 2);

    if (settings && findLine(/^Usage/i)) {
      return settings;
    }

    pressEscape();
  }

  throw new Error("The Assistant menu did not open");
}

function closeAssistantSettings(process) {
  const dialogs = process.windows.whose({ name: "Assistant Settings" });

  if (dialogs.length > 0) {
    dialogs[0].buttons.whose({ subrole: "AXCloseButton" })[0].click();
    delay(1);
  }
}

function waitForStatusChange(previous, seconds) {
  const deadline = Date.now() + seconds * 1000;

  do {
    const status = mcpStatus();

    if (status !== "unknown" && status !== previous) {
      return status;
    }

    delay(0.5);
  } while (Date.now() < deadline);

  return previous;
}

function setMcpSwitch(process, frame) {
  const prompt = openAssistantPanel(frame);
  const settings = openAssistantMenu(frame, prompt);
  const page = clickLabelUntil(settings, /^Settings$/i, /^MCP Servers$/i);

  if (!page) {
    throw new Error("Assistant Settings did not open");
  }

  const dialog = bounds(process.windows.whose({ name: "Assistant Settings" })[0]);

  click(page.x, page.y);

  // "Setup instructions", behind a chevron icon, appears only on the MCP Servers page, and the
  // server switch's row is the "Enable" line directly above it, so no other row can match.
  const instructions = waitFor(/Setup instructions/i, 6, dialog);
  const row = instructions && readScreen()
    .filter((line) => /^Enable/i.test(line.text) && contains(dialog, line))
    .filter((line) => line.y < instructions.y)
    .sort((a, b) => b.y - a.y)[0];

  if (!row) {
    throw new Error("The MCP server switch is not in Assistant Settings");
  }

  const before = mcpStatus();

  if (before === "unknown") {
    throw new Error("The MCP status is not readable, so a switch click could not be confirmed");
  }

  // The switch sits at the right end of its row, inside the dialog's padding. The first click
  // that changes the status is the switch, and nothing is clicked after it.
  for (let inset = 40; inset <= 90; inset += 6) {
    click(dialog.right - inset, row.y);

    if (waitForStatusChange(before, 4) !== before) {
      break;
    }
  }

  closeAssistantSettings(process);
}

function run(argv) {
  if (argv[0] === "read") {
    return readScreen()
      .map((line) => `${Math.round(line.x)},${Math.round(line.y)} ${line.text}`)
      .join("\n");
  }

  const pid = Number(argv[0]);
  const mode = argv[1];

  if (!Number.isInteger(pid) || !["on", "off"].includes(mode)) {
    throw new Error("Usage: guest_studio_mcp.js <studio-pid> on|off, or guest_studio_mcp.js read");
  }

  const target = mode === "off" ? "mcp off" : "mcp ready";
  const process = systemEvents.processes.whose({ unixId: pid })[0];

  if (mcpStatus() === target) {
    return `already ${target}`;
  }

  let failure = null;

  // Studio's web panels occasionally drop a click, so a failed pass starts over from a closed
  // dialog and a reset window.
  for (let attempt = 0; attempt < RUN_ATTEMPTS && mcpStatus() !== target; attempt++) {
    try {
      setMcpSwitch(process, resetStudioWindow(process));
    } catch (error) {
      failure = error;
      closeAssistantSettings(process);
      pressEscape();
    }
  }

  const status = mcpStatus();

  if (status !== target) {
    const cause = failure ? `; last step failed: ${failure.message}` : "";

    throw new Error(`Studio reports ${status}, expected ${target}${cause}`);
  }

  return status;
}
