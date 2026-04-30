#!/usr/bin/env python3
"""Trajectory Viewer — a lightweight local server to browse distilled VLM trajectories.

Usage:
    python viewer.py [--port PORT] [DATASET_DIR]

Opens a browser to view all trajectories under the dataset directory.
No external dependencies — stdlib only.
"""

import argparse
import json
import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote

# ---------------------------------------------------------------------------
# HTML template (embedded)
# ---------------------------------------------------------------------------

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Trajectory Viewer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0c0c0f;
  --surface: #16161a;
  --surface-hover: #1e1e24;
  --border: #2a2a32;
  --text: #e8e6e3;
  --text-muted: #8b8a87;
  --accent: #ff4d4f;
  --accent-glow: rgba(255, 77, 79, 0.25);
  --blue: #4fc3f7;
  --green: #66bb6a;
  --yellow: #fdd835;
  --radius: 10px;
  --font-mono: 'JetBrains Mono', monospace;
  --font-body: 'Noto Sans SC', system-ui, sans-serif;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-body);
  line-height: 1.6;
  min-height: 100vh;
}

/* Layout */
.app {
  display: grid;
  grid-template-columns: 320px 1fr;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  background: var(--surface);
  border-right: 1px solid var(--border);
  overflow-y: auto;
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 28px 24px 20px;
  border-bottom: 1px solid var(--border);
}

.sidebar-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.sidebar-header h1 {
  font-family: var(--font-mono);
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent);
  flex: 1;
}

.sidebar-header p {
  font-size: 12px;
  color: var(--text-muted);
  width: 100%;
}

.btn-icon {
  background: none;
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-muted);
  cursor: pointer;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: all 0.15s;
}

.btn-icon:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.btn-delete {
  background: none;
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-muted);
  cursor: pointer;
  padding: 6px 14px;
  font-size: 12px;
  font-family: var(--font-mono);
  transition: all 0.15s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-delete:hover {
  border-color: var(--accent);
  color: var(--accent);
  background: rgba(255, 77, 79, 0.08);
}

.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.confirm-dialog {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 28px 32px;
  max-width: 400px;
  text-align: center;
}

.confirm-dialog h3 {
  margin-bottom: 8px;
  font-size: 16px;
}

.confirm-dialog p {
  color: var(--text-muted);
  font-size: 13px;
  margin-bottom: 20px;
}

.confirm-dialog .actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.confirm-dialog button {
  padding: 8px 20px;
  border-radius: 6px;
  border: 1px solid var(--border);
  cursor: pointer;
  font-size: 13px;
  font-family: var(--font-body);
  transition: all 0.15s;
}

.confirm-dialog .btn-cancel {
  background: var(--surface-hover);
  color: var(--text);
}

.confirm-dialog .btn-cancel:hover {
  border-color: var(--text-muted);
}

.confirm-dialog .btn-confirm-delete {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}

.confirm-dialog .btn-confirm-delete:hover {
  background: #e04344;
}

.search-box {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
}

.search-box input {
  width: 100%;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 9px 12px 9px 34px;
  color: var(--text);
  font-size: 13px;
  font-family: var(--font-body);
  outline: none;
  transition: border-color 0.15s;
}

.search-box input:focus {
  border-color: var(--accent);
}

.search-box {
  position: relative;
}

.search-box::before {
  content: '\2315';
  position: absolute;
  left: 28px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  font-size: 15px;
  pointer-events: none;
}

.traj-item.hidden {
  display: none;
}

.group-label.hidden {
  display: none;
}

.group-label {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-muted);
  padding: 20px 24px 8px;
}

.traj-list {
  list-style: none;
  flex: 1;
  overflow-y: auto;
}

.traj-item {
  padding: 14px 24px;
  cursor: pointer;
  border-bottom: 1px solid var(--border);
  transition: background 0.15s;
}

.traj-item:hover {
  background: var(--surface-hover);
}

.traj-item.active {
  background: var(--surface-hover);
  border-left: 3px solid var(--accent);
  padding-left: 21px;
}

.traj-item .instruction {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.traj-item .meta {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
}

.traj-item .meta .steps-badge {
  background: var(--border);
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 6px;
}

/* Main content */
.main {
  padding: 40px 48px;
  overflow-y: auto;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 70vh;
  flex-direction: column;
  color: var(--text-muted);
}

.empty-state .icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.4;
}

/* Trajectory header */
.traj-header {
  margin-bottom: 40px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border);
}

.traj-header h2 {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 12px;
}

.traj-header .detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}

.detail-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 12px 16px;
}

.detail-card .label {
  font-family: var(--font-mono);
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.detail-card .value {
  font-size: 13px;
  font-weight: 500;
  word-break: break-all;
}

/* Timeline */
.timeline {
  position: relative;
  padding-left: 32px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 11px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--border);
}

.step {
  position: relative;
  margin-bottom: 48px;
  animation: fadeIn 0.3s ease both;
}

.step:last-child { margin-bottom: 0; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.step-dot {
  position: absolute;
  left: -32px;
  top: 4px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--surface);
  border: 2px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  color: var(--text-muted);
}

.step.terminal .step-dot {
  border-color: var(--green);
  color: var(--green);
}

.step.impossible .step-dot {
  border-color: var(--accent);
  color: var(--accent);
}

/* Thought bubble */
.thought {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 18px;
  margin-bottom: 16px;
  font-size: 14px;
  line-height: 1.7;
  position: relative;
}

.thought::before {
  content: 'THOUGHT';
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  position: absolute;
  top: -8px;
  left: 14px;
  background: var(--surface);
  padding: 0 6px;
}

/* Action badge */
.action-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 12px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 14px;
  margin-bottom: 16px;
}

.action-badge .action-type {
  background: var(--accent);
  color: #fff;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 11px;
}

.action-badge .action-type.type-finish { background: var(--green); }
.action-badge .action-type.type-impossible { background: var(--accent); }
.action-badge .action-type.type-click { background: #e040fb; }
.action-badge .action-type.type-swipe,
.action-badge .action-type.type-scroll { background: var(--blue); }
.action-badge .action-type.type-type { background: var(--yellow); color: #000; }
.action-badge .action-type.type-app_start { background: #78909c; }
.action-badge .action-type.type-press { background: #ab47bc; }

.action-params {
  color: var(--text-muted);
}

/* Screenshot container */
.screenshot-wrap {
  position: relative;
  display: inline-block;
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--border);
  max-width: 360px;
  background: #000;
}

.screenshot-wrap img {
  display: block;
  width: 100%;
  height: auto;
}

/* Overlay markers */
.click-marker {
  position: absolute;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--accent);
  border: 2px solid #fff;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 0 4px var(--accent-glow), 0 2px 8px rgba(0,0,0,0.5);
  pointer-events: none;
  z-index: 2;
}

.click-marker::after {
  content: '';
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  border: 1px solid rgba(255, 77, 79, 0.4);
  animation: ping 1.5s ease-out infinite;
}

@keyframes ping {
  0% { transform: scale(1); opacity: 0.6; }
  100% { transform: scale(1.8); opacity: 0; }
}

.swipe-arrow {
  position: absolute;
  z-index: 2;
  pointer-events: none;
}

.swipe-arrow line {
  stroke: var(--blue);
  stroke-width: 3;
  stroke-linecap: round;
}

.swipe-arrow polygon {
  fill: var(--blue);
}

/* Responsive */
@media (max-width: 900px) {
  .app { grid-template-columns: 1fr; }
  .sidebar {
    position: relative;
    height: auto;
    max-height: 40vh;
  }
  .main { padding: 24px 16px; }
}

.sidebar-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--border);
  font-size: 11px;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.sidebar-footer a {
  color: var(--accent);
  text-decoration: none;
  font-family: var(--font-mono);
  font-weight: 600;
  font-size: 11px;
}

.sidebar-footer a:hover {
  text-decoration: underline;
}
</style>
</head>
<body>
<div class="app">
  <aside class="sidebar">
    <div class="sidebar-header">
      <h1>Trajectory Viewer</h1>
      <button class="btn-icon" id="btn-refresh" title="Refresh">&#8635;</button>
      <p id="total-count"></p>
    </div>
    <div class="search-box">
      <input type="text" id="search-input" placeholder="Search trajectories..." autocomplete="off">
    </div>
    <ul class="traj-list" id="traj-list"></ul>
    <div class="sidebar-footer">
      <a href="https://github.com/lanbaoshen/QAMule" target="_blank">Powered by QAMule</a>
      <span>by <a href="https://github.com/lanbaoshen/" target="_blank">Lanbao Shen</a></span>
    </div>
  </aside>
  <main class="main" id="main">
    <div class="empty-state">
      <div class="icon">&#9712;</div>
      <p>Select a trajectory from the sidebar</p>
    </div>
  </main>
</div>

<script>
const BASE = '';

let allData = [];

async function loadIndex() {
  const res = await fetch(`${BASE}/api/trajectories`);
  allData = await res.json();
  renderList(allData);
  setupSearch();
}

function renderList(data) {
  const list = document.getElementById('traj-list');
  const total = data.reduce((s, g) => s + g.items.length, 0);
  document.getElementById('total-count').textContent = `${total} trajectories`;

  list.innerHTML = '';
  for (const group of data) {
    // Sort items within group by timestamp desc (extract from path)
    const sorted = [...group.items].sort((a, b) => {
      const ta = extractTimestamp(a.path);
      const tb = extractTimestamp(b.path);
      return tb.localeCompare(ta);
    });

    const label = document.createElement('li');
    label.className = 'group-label';
    label.textContent = group.group;
    list.appendChild(label);

    for (const item of sorted) {
      const li = document.createElement('li');
      li.className = 'traj-item';
      li.dataset.path = item.path;
      li.dataset.search = `${item.instruction} ${item.app} ${item.task_id} ${item.path}`.toLowerCase();
      li.innerHTML = `
        <div class="instruction">${esc(item.instruction)}</div>
        <div class="meta">${esc(item.app)}<span class="steps-badge">${item.steps} steps</span></div>
        <div class="meta" style="margin-top:2px;font-size:10px;opacity:0.7">${esc(item.task_id)}</div>
      `;
      li.addEventListener('click', () => selectTrajectory(li, item.path));
      list.appendChild(li);
    }
  }
}

function extractTimestamp(path) {
  // Path like "normal/cold_start_pin_unlock_20260430_113000/trajectory.json"
  const match = path.match(/(\d{8}_\d{6})/);
  return match ? match[1] : '0';
}

function setupSearch() {
  const input = document.getElementById('search-input');
  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase();
    const items = document.querySelectorAll('.traj-item');
    const labels = document.querySelectorAll('.group-label');

    if (!q) {
      items.forEach(el => el.classList.remove('hidden'));
      labels.forEach(el => el.classList.remove('hidden'));
      return;
    }

    items.forEach(el => {
      const match = el.dataset.search.includes(q);
      el.classList.toggle('hidden', !match);
    });

    // Hide group labels with no visible items after them
    labels.forEach(label => {
      let next = label.nextElementSibling;
      let hasVisible = false;
      while (next && !next.classList.contains('group-label')) {
        if (next.classList.contains('traj-item') && !next.classList.contains('hidden')) {
          hasVisible = true;
          break;
        }
        next = next.nextElementSibling;
      }
      label.classList.toggle('hidden', !hasVisible);
    });
  });
}

async function selectTrajectory(el, path) {
  document.querySelectorAll('.traj-item.active').forEach(e => e.classList.remove('active'));
  el.classList.add('active');

  const res = await fetch(`${BASE}/api/trajectory/${path}`);
  const traj = await res.json();
  renderTrajectory(traj, path);
}

function renderTrajectory(traj, basePath) {
  const main = document.getElementById('main');
  const dir = basePath.replace(/\/trajectory\.json$/, '');

  currentPath = basePath;

  let html = `<div class="traj-header">
    <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:12px">
      <h2 style="margin-bottom:0">${esc(traj.instruction)}</h2>
      <button class="btn-delete" onclick="deleteTrajectory('${basePath}')">&#128465; Delete</button>
    </div>
    <div class="detail-grid">
      <div class="detail-card"><div class="label">Task ID</div><div class="value">${esc(traj.task_id)}</div></div>
      <div class="detail-card"><div class="label">App</div><div class="value">${esc(traj.app)}</div></div>
      <div class="detail-card"><div class="label">Device</div><div class="value">${esc(traj.device?.model || '—')} · Android ${esc(String(traj.device?.android || ''))}</div></div>
      <div class="detail-card"><div class="label">Resolution</div><div class="value">${traj.device?.resolution ? traj.device.resolution.join(' × ') : '—'}</div></div>
      <div class="detail-card"><div class="label">Steps</div><div class="value">${traj.total_steps || traj.steps.length}</div></div>
    </div>
  </div>`;

  html += '<div class="timeline">';
  for (const step of traj.steps) {
    const isTerminal = step.action.type === 'finish';
    const isImpossible = step.action.type === 'impossible';
    const cls = isTerminal ? 'terminal' : isImpossible ? 'impossible' : '';

    html += `<div class="step ${cls}" style="animation-delay: ${step.step * 0.05}s">`;
    html += `<div class="step-dot">${step.step}</div>`;

    // Thought
    html += `<div class="thought">${esc(step.thought)}</div>`;

    // Action badge
    const actionType = step.action.type;
    const params = formatActionParams(step.action);
    html += `<div class="action-badge">
      <span class="action-type type-${actionType}">${actionType}</span>
      <span class="action-params">${esc(params)}</span>
    </div>`;

    // Screenshot with overlays
    if (step.screenshot) {
      html += `<div class="screenshot-wrap">`;
      html += `<img src="${BASE}/data/${dir}/${step.screenshot}" alt="Step ${step.step}" loading="lazy">`;

      // Click marker overlay (shown on NEXT step's screenshot if action is click)
      // Actually we show on current screenshot where the action will be performed
      if ((actionType === 'click' || actionType === 'long_click') && step.action.x != null) {
        const x = step.action.x / 10; // 0-1000 -> 0-100%
        const y = step.action.y / 10;
        html += `<div class="click-marker" style="left:${x}%;top:${y}%"></div>`;
      }

      if (actionType === 'swipe' && step.action.x1 != null) {
        const x1 = step.action.x1 / 10, y1 = step.action.y1 / 10;
        const x2 = step.action.x2 / 10, y2 = step.action.y2 / 10;
        html += renderSwipeArrow(x1, y1, x2, y2);
      }

      html += `</div>`;
    }

    html += `</div>`;
  }
  html += '</div>';

  main.innerHTML = html;
  main.scrollTop = 0;
}

function formatActionParams(action) {
  switch (action.type) {
    case 'click':
    case 'long_click':
      return `(${action.x}, ${action.y})`;
    case 'swipe':
      return `(${action.x1},${action.y1}) → (${action.x2},${action.y2})`;
    case 'scroll':
      return action.direction;
    case 'type':
      return `"${action.text}"`;
    case 'press':
      return action.key;
    case 'app_start':
      return action.app;
    case 'finish':
    case 'impossible':
      return action.reason || '';
    default:
      return JSON.stringify(action);
  }
}

function renderSwipeArrow(x1, y1, x2, y2) {
  return `<svg class="swipe-arrow" style="position:absolute;inset:0;width:100%;height:100%;" viewBox="0 0 100 100" preserveAspectRatio="none">
    <defs><marker id="ah" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
      <polygon points="0 0, 6 2, 0 4" fill="#4fc3f7"/>
    </marker></defs>
    <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" marker-end="url(#ah)" stroke="#4fc3f7" stroke-width="0.6" stroke-linecap="round"/>
  </svg>`;
}

function esc(s) {
  if (!s) return '';
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

document.getElementById('btn-refresh').addEventListener('click', () => loadIndex());

let currentPath = null;

async function deleteTrajectory(path) {
  const overlay = document.createElement('div');
  overlay.className = 'confirm-overlay';
  overlay.innerHTML = `
    <div class="confirm-dialog">
      <h3>Delete Trajectory</h3>
      <p>This will permanently delete the trajectory and all its screenshots. This cannot be undone.</p>
      <div class="actions">
        <button class="btn-cancel">Cancel</button>
        <button class="btn-confirm-delete">Delete</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  overlay.querySelector('.btn-cancel').addEventListener('click', () => overlay.remove());
  overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });

  overlay.querySelector('.btn-confirm-delete').addEventListener('click', async () => {
    overlay.remove();
    const res = await fetch(`${BASE}/api/trajectory/${path}`, { method: 'DELETE' });
    if (res.ok) {
      currentPath = null;
      document.getElementById('main').innerHTML = `<div class="empty-state"><div class="icon">&#9712;</div><p>Trajectory deleted</p></div>`;
      loadIndex();
    } else {
      alert('Failed to delete: ' + (await res.text()));
    }
  });
}

loadIndex();
</script>
</body>
</html>"""


class ViewerHandler(SimpleHTTPRequestHandler):
    """HTTP request handler with API routes for trajectory viewing."""

    dataset_dir: Path  # set by class factory

    def do_GET(self):
        path = unquote(self.path.split("?")[0])

        if path == "/" or path == "":
            self._serve_html()
        elif path == "/api/trajectories":
            self._serve_index()
        elif path.startswith("/api/trajectory/"):
            rel = path[len("/api/trajectory/"):]
            self._serve_trajectory(rel)
        elif path.startswith("/data/"):
            rel = path[len("/data/"):]
            self._serve_file(rel)
        else:
            self.send_error(404)

    def do_DELETE(self):
        path = unquote(self.path.split("?")[0])
        if path.startswith("/api/trajectory/"):
            rel = path[len("/api/trajectory/"):]
            self._delete_trajectory(rel)
        else:
            self.send_error(404)

    def _serve_html(self):
        content = HTML_PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _serve_index(self):
        """Scan dataset directory and return grouped trajectory list."""
        result = []
        dataset = self.dataset_dir

        for scenario_type in sorted(dataset.iterdir()):
            if not scenario_type.is_dir():
                continue
            group = {"group": scenario_type.name, "items": []}
            for session in sorted(scenario_type.iterdir()):
                traj_file = session / "trajectory.json"
                if not traj_file.exists():
                    continue
                try:
                    data = json.loads(traj_file.read_text(encoding="utf-8"))
                    group["items"].append(
                        {
                            "path": f"{scenario_type.name}/{session.name}/trajectory.json",
                            "task_id": data.get("task_id", ""),
                            "instruction": data.get("instruction", "—"),
                            "app": data.get("app", ""),
                            "steps": data.get("total_steps", len(data.get("steps", []))),
                        }
                    )
                except (json.JSONDecodeError, OSError):
                    continue
            if group["items"]:
                result.append(group)

        self._send_json(result)

    def _serve_trajectory(self, rel_path: str):
        """Return a single trajectory.json."""
        target = self.dataset_dir / rel_path
        if not target.exists() or not target.is_file():
            self.send_error(404)
            return
        # Prevent path traversal
        try:
            target.resolve().relative_to(self.dataset_dir.resolve())
        except ValueError:
            self.send_error(403)
            return

        try:
            data = json.loads(target.read_text(encoding="utf-8"))
            self._send_json(data)
        except (json.JSONDecodeError, OSError) as e:
            self.send_error(500, str(e))

    def _delete_trajectory(self, rel_path: str):
        """Delete a trajectory directory (json + screenshots)."""
        import shutil

        target = self.dataset_dir / rel_path
        if not target.exists():
            self.send_error(404)
            return
        # Prevent path traversal
        try:
            target.resolve().relative_to(self.dataset_dir.resolve())
        except ValueError:
            self.send_error(403)
            return

        # Delete the entire session directory
        session_dir = target.parent
        try:
            shutil.rmtree(session_dir)
        except OSError as e:
            self.send_error(500, str(e))
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok": true}')

    def _serve_file(self, rel_path: str):
        """Serve a static file (screenshot) from the dataset directory."""
        target = self.dataset_dir / rel_path
        if not target.exists() or not target.is_file():
            self.send_error(404)
            return
        # Prevent path traversal
        try:
            target.resolve().relative_to(self.dataset_dir.resolve())
        except ValueError:
            self.send_error(403)
            return

        ext = target.suffix.lower()
        content_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
            ".gif": "image/gif",
        }
        ct = content_types.get(ext, "application/octet-stream")

        content = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "public, max-age=3600")
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, data):
        content = json.dumps(data, ensure_ascii=False, indent=None).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        # Quieter logging
        pass


def make_handler(dataset_dir: Path):
    """Create a handler class bound to a specific dataset directory."""

    class BoundHandler(ViewerHandler):
        pass

    BoundHandler.dataset_dir = dataset_dir
    return BoundHandler


def main():
    parser = argparse.ArgumentParser(description="Trajectory Viewer")
    parser.add_argument("dataset_dir", nargs="?", default=".", help="Path to the dataset directory")
    parser.add_argument("--port", type=int, default=8932, help="Port to serve on")
    parser.add_argument("--no-open", action="store_true", help="Don't open browser automatically")
    args = parser.parse_args()

    dataset_dir = Path(args.dataset_dir).resolve()
    if not dataset_dir.is_dir():
        print(f"Error: {dataset_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    handler = make_handler(dataset_dir)
    server = HTTPServer(("127.0.0.1", args.port), handler)

    url = f"http://127.0.0.1:{args.port}"
    print(f"Serving trajectories from: {dataset_dir}")
    print(f"Viewer running at: {url}")
    print("Press Ctrl+C to stop.\n")

    if not args.no_open:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.shutdown()


if __name__ == "__main__":
    main()
