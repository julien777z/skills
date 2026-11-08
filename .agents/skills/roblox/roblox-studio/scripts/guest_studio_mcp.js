// Turn Roblox Studio's MCP server on or off from inside a macOS guest, without a viewer.
//
// Run in the guest's signed-in session, from a process the guest grants Accessibility
// (for example `osascript` over SSH on a Cirrus Labs image):
//
//   osascript -l JavaScript guest_studio_mcp.js <studio-pid> on|off|read
//
// `read` prints each recognized line with its center in screen points.
//
// It finds controls by their on-screen text with Vision, clicks in screen points, and
// prints the final status-bar state. Exit status is nonzero when the target state is
// not reached.

ObjC.import("AppKit");
ObjC.import("CoreGraphics");
ObjC.import("Vision");

const CAPTURE_PATH = "/tmp/guest-studio-mcp.png";
const STEP_DELAY_SECONDS = 2;

// The Assistant toolbar button and its panel menu carry no text, so they are found
// relative to the window's right edge and the panel's title.
const ASSISTANT_BUTTON_FROM_RIGHT = 94;
const ASSISTANT_BUTTON_FROM_TOP = 50;
const PANEL_MENU_FROM_RIGHT = 21;
const PANEL_MENU_BELOW_TITLE = 36;
const SWITCH_FROM_DIALOG_RIGHT = 58;

const systemEvents = Application("System Events");
const source = $.CGEventSourceCreate($.kCGEventSourceStateHIDSystemState);

function studioProcess(pid) {
  return systemEvents.processes.whose({ unixId: pid })[0];
}

// Studio can hold a stale window origin and register clicks below where they land on
// screen; setting the frame again makes it recompute.
function resetStudioWindow(process) {
  process.frontmost = true;

  const window = process.windows.whose({ name: { _contains: "Roblox Studio" } })[0];
  const [x, y] = window.position();
  const [width, height] = window.size();

  window.position = [x, y + 8];
  delay(0.4);
  window.position = [x, y];
  window.size = [width, height];
  delay(0.6);

  return { x, y, width, height };
}

function postMouse(type, x, y) {
  const event = $.CGEventCreateMouseEvent(source, type, $.CGPointMake(x, y), $.kCGMouseButtonLeft);

  // Studio's widgets ignore a press without a click count.
  $.CGEventSetIntegerValueField(event, $.kCGMouseEventClickState, 1);
  $.CGEventPost($.kCGHIDEventTap, event);
}

function click(x, y) {
  for (const step of [12, 6, 0]) {
    postMouse($.kCGEventMouseMoved, x - step, y + step);
    delay(0.12);
  }

  postMouse($.kCGEventLeftMouseDown, x, y);
  delay(0.1);
  postMouse($.kCGEventLeftMouseUp, x, y);
  delay(STEP_DELAY_SECONDS);
}

// Returns recognized lines with centers in screen points.
function readScreen() {
  const task = $.NSTask.launchedTaskWithLaunchPathArguments("/usr/sbin/screencapture", $(["-x", CAPTURE_PATH]));

  task.waitUntilExit;

  const screen = $.NSScreen.mainScreen.frame.size;
  const url = $.NSURL.fileURLWithPath(CAPTURE_PATH);
  const request = $.VNRecognizeTextRequest.alloc.init;
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
      left: box.origin.x * screen.width,
    });
  }

  return lines;
}

function findLine(pattern) {
  return readScreen().find((line) => pattern.test(line.text));
}

function mcpStatus() {
  const line = findLine(/MCP (Ready|off)/i);

  return line ? line.text.match(/MCP (Ready|off)/i)[0].toLowerCase() : "unknown";
}

function openAssistantPanel(frame) {
  if (findLine(/^Ask Assistant$/)) {
    return;
  }

  click(frame.x + frame.width - ASSISTANT_BUTTON_FROM_RIGHT, frame.y + ASSISTANT_BUTTON_FROM_TOP);

  if (!findLine(/^Ask Assistant$/)) {
    throw new Error("The Assistant panel did not open");
  }
}

function openMcpServersPage(process, frame) {
  const title = readScreen().find((line) => line.text === "Assistant" && line.x > frame.x + frame.width / 2);

  if (!title) {
    throw new Error("The Assistant panel title is not on screen");
  }

  const menuX = frame.x + frame.width - PANEL_MENU_FROM_RIGHT;
  const menuY = title.y + PANEL_MENU_BELOW_TITLE;

  // The panel's web view can swallow the first click while it takes focus.
  for (let attempt = 0; attempt < 2 && !findLine(/^Settings$/); attempt++) {
    click(menuX, menuY);
  }

  const settings = findLine(/^Settings$/);

  if (!settings) {
    throw new Error("The Assistant menu did not open");
  }

  click(settings.x, settings.y);

  const page = findLine(/^MCP Servers$/);

  if (!page) {
    throw new Error("Assistant Settings did not open");
  }

  click(page.x, page.y);

  return process.windows.whose({ name: "Assistant Settings" })[0];
}

function run(argv) {
  if (argv[1] === "read") {
    return readScreen().map((line) => `${Math.round(line.x)},${Math.round(line.y)} ${line.text}`).join("\n");
  }

  const pid = Number(argv[0]);
  const target = argv[1] === "off" ? "mcp off" : "mcp ready";
  const process = studioProcess(pid);
  const frame = resetStudioWindow(process);

  if (mcpStatus() === target) {
    return `already ${target}`;
  }

  openAssistantPanel(frame);

  const dialog = openMcpServersPage(process, frame);
  const row = findLine(/^Enable/);

  if (!row) {
    throw new Error("The MCP server switch is not on screen");
  }

  const [dialogX] = dialog.position();
  const [dialogWidth] = dialog.size();

  click(dialogX + dialogWidth - SWITCH_FROM_DIALOG_RIGHT, row.y);

  dialog.buttons.whose({ subrole: "AXCloseButton" })[0].click();
  delay(STEP_DELAY_SECONDS);

  const status = mcpStatus();

  if (status !== target) {
    throw new Error(`Studio reports ${status}, expected ${target}`);
  }

  return status;
}
