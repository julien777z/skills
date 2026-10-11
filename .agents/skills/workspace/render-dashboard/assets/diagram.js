var PALETTE_TOKENS = ["--bg", "--surface", "--ink", "--ink-2", "--muted", "--line", "--good", "--accent", "--critical", "--font-sans"];
var MERMAID_SCRIPT = {
  src: "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js",
  integrity: "sha384-rbtjAdnIQE/aQJGEgXrVUlMibdfTSa4PQju4HDhN3sR2PmaKFzhEafuePsl9H/9I"
};
var MIN_DIAGRAM_SCALE = 0.65;
var SPLIT_RATIO = 0.6;
var RANK_SPACING = {
  LR: '%%{init: {"flowchart": {"rankSpacing": 36}}}%%',
  TB: '%%{init: {"flowchart": {"rankSpacing": 60}}}%%'
};
var mermaidReady = null;
var diagramCount = 0;

function palette() {
  var styles = getComputedStyle(document.documentElement);
  var colors = {};

  PALETTE_TOKENS.forEach(function (name) { colors[name] = styles.getPropertyValue(name).trim(); });

  return colors;
}

function loadMermaid() {
  if (!mermaidReady) {
    mermaidReady = new Promise(function (resolve, reject) {
      var script = document.createElement("script");

      script.src = MERMAID_SCRIPT.src;
      script.integrity = MERMAID_SCRIPT.integrity;
      script.crossOrigin = "anonymous";
      script.onload = function () { resolve(window.mermaid); };
      script.onerror = function () { reject(new Error("Mermaid did not load")); };
      document.head.append(script);
    }).then(function (mermaid) {
      var colors = palette();

      mermaid.initialize({
        startOnLoad: false,
        securityLevel: "strict",
        theme: "base",
        fontFamily: colors["--font-sans"],
        flowchart: { curve: "basis", padding: 10, nodeSpacing: 28, wrappingWidth: 400 },
        themeVariables: {
          fontSize: "14px",
          primaryColor: colors["--surface"],
          primaryTextColor: colors["--ink"],
          primaryBorderColor: colors["--line"],
          lineColor: colors["--muted"],
          clusterBkg: colors["--bg"],
          clusterBorder: colors["--line"],
          titleColor: colors["--muted"],
          edgeLabelBackground: colors["--surface"]
        }
      });

      return { mermaid: mermaid, colors: colors };
    });
  }

  return mermaidReady;
}

function mermaidString(value) {
  return value.replace(/`/g, "").replace(/[&<>"#%]/g, function (character) { return "#" + character.charCodeAt(0) + ";"; });
}

function strokeStyle(style, colors) {
  return "stroke:" + colors[style.token] + ",stroke-width:" + style.width + (style.dashed ? ",stroke-dasharray:5 4" : "");
}

function flowchartSource(section, direction, colors) {
  var ids = Object.create(null);
  var lines = [RANK_SPACING[direction], "flowchart " + direction];

  section.nodes.forEach(function (node, index) { ids[node.id] = "n" + index; });

  function nodeLine(node) {
    var text = "<b>" + mermaidString(node.label) + "</b>";

    if (node.detail) text += "<br/><small>" + mermaidString(node.detail) + "</small>";

    return ids[node.id] + "[\"" + text + "\"]:::" + (node.change || "same");
  }

  section.nodes.filter(function (node) { return !node.pr; }).forEach(function (node) { lines.push(nodeLine(node)); });

  (section.prs || []).forEach(function (entry, index) {
    lines.push("subgraph pr" + index + "[\"" + mermaidString(entry.ref) + "\"]");
    section.nodes.filter(function (node) { return node.pr === entry.ref; }).forEach(function (node) { lines.push("  " + nodeLine(node)); });
    lines.push("end");
  });

  section.edges.forEach(function (edge) {
    var label = [edge.step, edge.label].filter(Boolean).join(" · ");

    lines.push(ids[edge.from] + " --> " + (label ? "|\"" + mermaidString(String(label)) + "\"| " : "") + ids[edge.to]);
  });

  section.edges.forEach(function (edge, index) {
    if (edge.change) lines.push("linkStyle " + index + " " + strokeStyle(CHANGE_STYLES[edge.change], colors));
  });

  Object.keys(CHANGE_STYLES).forEach(function (change) {
    var style = CHANGE_STYLES[change];

    lines.push("classDef " + change + " fill:" + colors["--surface"] + ",color:" + colors[style.text] + "," + strokeStyle(style, colors));
  });

  return lines.join("\n");
}

function pickDrawing(results, available) {
  var drawings = results.map(function (result) {
    var holder = document.createElement("div");

    holder.innerHTML = result.svg;

    var svg = holder.querySelector("svg");
    var width = svg.viewBox.baseVal.width;

    return { svg: svg, width: width, scale: Math.min(1, available / width) };
  });

  var preferred = drawings[0];
  var readable = preferred.scale >= MIN_DIAGRAM_SCALE || preferred.scale >= drawings[1].scale;

  return readable ? preferred : drawings[1];
}

function drawDiagram(section, wrap, figure, hasSteps) {
  var id = "diagram-" + diagramCount++;

  loadMermaid().then(function (ready) {
    return Promise.all(["LR", "TB"].map(function (direction) {
      return ready.mermaid.render(id + "-" + direction, flowchartSource(section, direction, ready.colors));
    }));
  }).then(function (results) {
    var available = figure.clientWidth;
    var drawing = pickDrawing(results, available);
    var drawnWidth = drawing.width * Math.max(drawing.scale, MIN_DIAGRAM_SCALE);

    drawing.svg.style.maxWidth = "none";
    drawing.svg.style.width = Math.round(drawnWidth) + "px";

    figure.replaceChildren(drawing.svg);
    figure.scrollLeft = (figure.scrollWidth - figure.clientWidth) / 2;

    linkReferences(figure);

    if (hasSteps && drawnWidth < available * SPLIT_RATIO) wrap.classList.add("split");
  }).catch(function (error) {
    console.error(error);

    figure.prepend(el("p", "empty", "The diagram could not be drawn, so its connections are listed instead."));
  });
}

function diagramFallback(section) {
  var labels = Object.create(null);
  var list = el("ul", "diagram-fallback");

  section.nodes.forEach(function (node) { labels[node.id] = node.label; });

  section.edges.forEach(function (edge) {
    list.append(el("li", "", labels[edge.from] + " → " + labels[edge.to] + (edge.label ? ": " + edge.label : "")));
  });

  return list;
}

function diagramLegend(section) {
  var used = section.nodes.concat(section.edges).map(function (part) { return part.change; });
  var changes = Object.keys(CHANGE_STYLES).filter(function (change) { return used.indexOf(change) >= 0; });

  if (!changes.length) return null;

  var legend = el("div", "key-row");

  changes.concat(["same"]).forEach(function (change) {
    var style = CHANGE_STYLES[change];
    var key = el("span");
    var swatch = el("span", "swatch");

    swatch.style.borderColor = "var(" + (style.swatch || style.token) + ")";
    swatch.style.borderStyle = style.dashed ? "dashed" : "solid";
    key.append(swatch, document.createTextNode(style.label));
    legend.append(key);
  });

  return legend;
}

function diagramPullRequests(pullRequests) {
  var row = el("div", "key-row");

  pullRequests.forEach(function (entry) {
    row.append(link(entry.ref, entry.url));
  });

  return row;
}

function diagramSteps(steps) {
  var list = el("ol", "diagram-steps");

  steps.forEach(function (step, position) {
    var item = el("li");

    item.append(el("span", "glyph", String(position + 1)), el("span", "", step));
    list.append(item);
  });

  return list;
}

function diagramSection(section, draws) {
  var wrap = el("div", "diagram panel");
  var canvas = el("div", "diagram-canvas");
  var figure = el("div", "diagram-figure");
  var legend = diagramLegend(section);
  var hasSteps = Boolean(section.steps);

  figure.append(diagramFallback(section));
  canvas.append(figure);

  if (legend) canvas.append(legend);

  if (section.prs) canvas.append(diagramPullRequests(section.prs));

  wrap.append(canvas);

  if (hasSteps) wrap.append(diagramSteps(section.steps));

  draws.push(function () { drawDiagram(section, wrap, figure, hasSteps); });

  return wrap;
}
