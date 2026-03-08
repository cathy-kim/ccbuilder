#!/usr/bin/env python3
"""
Eval viewer — HTTP server and standalone HTML generator for reviewing eval outputs.

Usage:
    # Start server
    python eval-viewer/generate_review.py <workspace>/iteration-N \
        --skill-name "my-skill" \
        --benchmark <workspace>/iteration-N/benchmark.json

    # Generate static HTML
    python eval-viewer/generate_review.py <workspace>/iteration-N \
        --skill-name "my-skill" \
        --static output.html

    # With previous iteration context
    python eval-viewer/generate_review.py <workspace>/iteration-2 \
        --skill-name "my-skill" \
        --previous-workspace <workspace>/iteration-1
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import signal
import subprocess
import sys
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".py", ".ts", ".js", ".tsx", ".jsx",
    ".yaml", ".yml", ".toml", ".html", ".css", ".sh", ".bash",
    ".sql", ".xml", ".csv", ".env", ".cfg", ".ini", ".log",
}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico"}


def find_runs(workspace: Path) -> list[dict]:
    """Recursively discover directories containing outputs/ subdirectory."""
    runs = []
    for root, dirs, files in os.walk(workspace):
        root_path = Path(root)
        if "outputs" in dirs:
            run_info = {"path": root_path, "id": root_path.name}

            # Read eval_metadata.json if exists
            meta_path = root_path / "eval_metadata.json"
            if meta_path.exists():
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                run_info["eval_id"] = meta.get("eval_id", 0)
                run_info["eval_name"] = meta.get("eval_name", run_info["id"])
                run_info["prompt"] = meta.get("prompt", "")
            else:
                run_info["eval_id"] = 0
                run_info["eval_name"] = run_info["id"]
                run_info["prompt"] = ""

            runs.append(run_info)

    runs.sort(key=lambda r: (r.get("eval_id", 0), r["id"]))
    return runs


def embed_file(file_path: Path) -> dict:
    """Embed a file's content based on its type."""
    suffix = file_path.suffix.lower()

    if suffix in TEXT_EXTENSIONS:
        try:
            content = file_path.read_text(encoding="utf-8")
            return {"type": "text", "name": file_path.name, "content": content, "extension": suffix}
        except UnicodeDecodeError:
            pass

    if suffix in IMAGE_EXTENSIONS:
        data = file_path.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        mime = {
            ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".gif": "image/gif", ".svg": "image/svg+xml", ".webp": "image/webp",
        }.get(suffix, "application/octet-stream")
        return {"type": "image", "name": file_path.name, "data_uri": f"data:{mime};base64,{b64}"}

    if suffix == ".pdf":
        data = file_path.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        return {"type": "pdf", "name": file_path.name, "data_uri": f"data:application/pdf;base64,{b64}"}

    # Binary fallback
    data = file_path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return {"type": "binary", "name": file_path.name, "data_b64": b64, "size": len(data)}


def build_run(run_info: dict) -> dict:
    """Assemble run data with embedded outputs and grading."""
    run_path = run_info["path"]
    outputs_dir = run_path / "outputs"

    outputs = []
    if outputs_dir.exists():
        for f in sorted(outputs_dir.iterdir()):
            if f.is_file() and not f.name.startswith("."):
                outputs.append(embed_file(f))

    grading = None
    grading_path = run_path / "grading.json"
    if grading_path.exists():
        with open(grading_path, "r", encoding="utf-8") as f:
            grading = json.load(f)

    timing = None
    timing_path = run_path / "timing.json"
    if timing_path.exists():
        with open(timing_path, "r", encoding="utf-8") as f:
            timing = json.load(f)

    return {
        "id": run_info["id"],
        "eval_id": run_info.get("eval_id", 0),
        "eval_name": run_info.get("eval_name", run_info["id"]),
        "prompt": run_info.get("prompt", ""),
        "outputs": outputs,
        "grading": grading,
        "timing": timing,
    }


def load_previous(prev_workspace: Path | None) -> dict | None:
    """Load previous iteration's runs and feedback."""
    if not prev_workspace or not prev_workspace.exists():
        return None

    prev_runs = find_runs(prev_workspace)
    prev_data = [build_run(r) for r in prev_runs]

    feedback = None
    feedback_path = prev_workspace / "feedback.json"
    if feedback_path.exists():
        with open(feedback_path, "r", encoding="utf-8") as f:
            feedback = json.load(f)

    return {"runs": prev_data, "feedback": feedback}


def generate_html(
    workspace: Path,
    skill_name: str,
    benchmark_path: Path | None = None,
    previous_workspace: Path | None = None,
) -> str:
    """Generate the complete HTML viewer."""
    runs = find_runs(workspace)
    run_data = [build_run(r) for r in runs]

    benchmark = None
    if benchmark_path and benchmark_path.exists():
        with open(benchmark_path, "r", encoding="utf-8") as f:
            benchmark = json.load(f)

    previous = load_previous(previous_workspace)

    feedback = {}
    feedback_path = workspace / "feedback.json"
    if feedback_path.exists():
        with open(feedback_path, "r", encoding="utf-8") as f:
            feedback = json.load(f)

    data = {
        "skill_name": skill_name,
        "generated_at": datetime.now().isoformat(),
        "runs": run_data,
        "benchmark": benchmark,
        "previous": previous,
        "feedback": feedback,
    }

    # Read the viewer template
    viewer_template = Path(__file__).parent / "viewer.html"
    if viewer_template.exists():
        html = viewer_template.read_text(encoding="utf-8")
        html = html.replace("__EMBEDDED_DATA_PLACEHOLDER__", json.dumps(data, ensure_ascii=False, indent=2))
        return html

    # Fallback: inline template
    return _inline_template(data)


def _inline_template(data: dict) -> str:
    """Generate a self-contained HTML page with embedded data."""
    data_json = json.dumps(data, ensure_ascii=False, indent=2)
    skill_name = data["skill_name"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{skill_name} — Eval Viewer</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0d1117; color: #c9d1d9; }}
.header {{ background: #161b22; border-bottom: 1px solid #30363d; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; }}
.header h1 {{ font-size: 20px; color: #58a6ff; }}
.tabs {{ display: flex; gap: 0; margin: 0 24px; }}
.tab {{ padding: 12px 24px; cursor: pointer; border-bottom: 2px solid transparent; color: #8b949e; font-weight: 500; }}
.tab.active {{ color: #58a6ff; border-bottom-color: #58a6ff; }}
.tab:hover {{ color: #c9d1d9; }}
.content {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}
.eval-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; margin-bottom: 16px; overflow: hidden; }}
.eval-header {{ padding: 16px; background: #1c2128; border-bottom: 1px solid #30363d; cursor: pointer; display: flex; justify-content: space-between; }}
.eval-header h3 {{ color: #58a6ff; }}
.eval-body {{ padding: 16px; display: none; }}
.eval-body.open {{ display: block; }}
.prompt {{ background: #0d1117; padding: 12px; border-radius: 6px; margin-bottom: 12px; font-family: monospace; font-size: 13px; white-space: pre-wrap; }}
.output-file {{ margin: 8px 0; }}
.output-file h4 {{ color: #8b949e; font-size: 13px; margin-bottom: 4px; }}
.output-file pre {{ background: #0d1117; padding: 12px; border-radius: 6px; font-size: 13px; overflow-x: auto; max-height: 400px; overflow-y: auto; }}
.output-file img {{ max-width: 100%; border-radius: 6px; }}
.grading {{ margin-top: 12px; }}
.expectation {{ padding: 6px 12px; margin: 4px 0; border-radius: 4px; font-size: 13px; }}
.expectation.pass {{ background: rgba(63, 185, 80, 0.1); border-left: 3px solid #3fb950; }}
.expectation.fail {{ background: rgba(248, 81, 73, 0.1); border-left: 3px solid #f85149; }}
.evidence {{ color: #8b949e; font-size: 12px; margin-top: 2px; }}
.feedback-area {{ margin-top: 12px; }}
.feedback-area textarea {{ width: 100%; min-height: 80px; background: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #c9d1d9; padding: 8px; font-family: inherit; font-size: 14px; resize: vertical; }}
.feedback-area textarea:focus {{ outline: none; border-color: #58a6ff; }}
.summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
.summary-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; text-align: center; }}
.summary-card .value {{ font-size: 28px; font-weight: 700; }}
.summary-card .label {{ color: #8b949e; font-size: 13px; margin-top: 4px; }}
.pass-rate {{ color: #3fb950; }}
.benchmark-table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
.benchmark-table th, .benchmark-table td {{ padding: 10px 16px; text-align: left; border-bottom: 1px solid #30363d; font-size: 13px; }}
.benchmark-table th {{ background: #1c2128; color: #8b949e; font-weight: 600; }}
.btn {{ padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500; }}
.btn-primary {{ background: #238636; color: white; }}
.btn-primary:hover {{ background: #2ea043; }}
.nav {{ display: flex; gap: 8px; justify-content: center; margin: 16px 0; }}
.nav .btn {{ background: #21262d; color: #c9d1d9; border: 1px solid #30363d; }}
.nav .btn:hover {{ background: #30363d; }}
.hidden {{ display: none; }}
.prev-section {{ border-left: 3px solid #8b949e; padding-left: 12px; margin-top: 12px; opacity: 0.7; }}
.prev-section summary {{ cursor: pointer; color: #8b949e; font-size: 13px; }}
</style>
</head>
<body>
<div class="header">
  <h1>{skill_name} — Eval Review</h1>
  <div>
    <button class="btn btn-primary" onclick="submitFeedback()">Submit All Reviews</button>
  </div>
</div>
<div class="tabs">
  <div class="tab active" onclick="switchTab('outputs')">Outputs</div>
  <div class="tab" onclick="switchTab('benchmark')">Benchmark</div>
</div>
<div id="tab-outputs" class="content"></div>
<div id="tab-benchmark" class="content hidden"></div>

<script>
const DATA = {data_json};

function switchTab(name) {{
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.content').forEach(c => c.classList.add('hidden'));
  event.target.classList.add('active');
  document.getElementById('tab-' + name).classList.remove('hidden');
}}

function renderOutputs() {{
  const container = document.getElementById('tab-outputs');
  const runs = DATA.runs || [];

  if (runs.length === 0) {{
    container.innerHTML = '<p style="color:#8b949e;text-align:center;padding:40px;">No runs found in workspace.</p>';
    return;
  }}

  // Summary
  let totalPass = 0, totalFail = 0, totalExpectations = 0;
  runs.forEach(r => {{
    if (r.grading && r.grading.summary) {{
      totalPass += r.grading.summary.passed || 0;
      totalFail += r.grading.summary.failed || 0;
      totalExpectations += r.grading.summary.total || 0;
    }}
  }});

  let html = '<div class="summary">';
  html += `<div class="summary-card"><div class="value">${{runs.length}}</div><div class="label">Test Runs</div></div>`;
  if (totalExpectations > 0) {{
    const rate = ((totalPass / totalExpectations) * 100).toFixed(1);
    html += `<div class="summary-card"><div class="value pass-rate">${{rate}}%</div><div class="label">Pass Rate (${{totalPass}}/${{totalExpectations}})</div></div>`;
  }}
  html += '</div>';

  runs.forEach((run, idx) => {{
    const isOpen = idx === 0 ? 'open' : '';
    html += `<div class="eval-card">`;
    html += `<div class="eval-header" onclick="this.nextElementSibling.classList.toggle('open')">`;
    html += `<h3>${{run.eval_name || run.id}}</h3>`;
    if (run.grading && run.grading.summary) {{
      const s = run.grading.summary;
      const color = s.pass_rate >= 0.8 ? '#3fb950' : s.pass_rate >= 0.5 ? '#d29922' : '#f85149';
      html += `<span style="color:${{color}};font-weight:600">${{s.passed}}/${{s.total}} passed</span>`;
    }}
    html += `</div>`;
    html += `<div class="eval-body ${{isOpen}}">`;

    if (run.prompt) {{
      html += `<div class="prompt">${{escapeHtml(run.prompt)}}</div>`;
    }}

    // Outputs
    (run.outputs || []).forEach(out => {{
      html += `<div class="output-file"><h4>${{escapeHtml(out.name)}}</h4>`;
      if (out.type === 'text') {{
        html += `<pre>${{escapeHtml(out.content)}}</pre>`;
      }} else if (out.type === 'image') {{
        html += `<img src="${{out.data_uri}}" alt="${{out.name}}">`;
      }} else {{
        html += `<pre>[Binary file: ${{out.name}}, ${{out.size || '?'}} bytes]</pre>`;
      }}
      html += `</div>`;
    }});

    // Grading
    if (run.grading && run.grading.expectations) {{
      html += `<div class="grading"><h4 style="color:#8b949e;margin-bottom:8px;">Assertions</h4>`;
      run.grading.expectations.forEach(exp => {{
        const cls = exp.passed ? 'pass' : 'fail';
        const icon = exp.passed ? '\u2705' : '\u274c';
        html += `<div class="expectation ${{cls}}">${{icon}} ${{escapeHtml(exp.text)}}`;
        if (exp.evidence) {{
          html += `<div class="evidence">${{escapeHtml(exp.evidence)}}</div>`;
        }}
        html += `</div>`;
      }});
      html += `</div>`;
    }}

    // Previous
    if (DATA.previous) {{
      const prevRun = (DATA.previous.runs || []).find(p => p.eval_name === run.eval_name || p.id === run.id);
      if (prevRun) {{
        html += `<details class="prev-section"><summary>Previous Iteration Output</summary>`;
        (prevRun.outputs || []).forEach(out => {{
          html += `<div class="output-file"><h4>${{escapeHtml(out.name)}}</h4>`;
          if (out.type === 'text') html += `<pre>${{escapeHtml(out.content)}}</pre>`;
          html += `</div>`;
        }});
        if (DATA.previous.feedback && DATA.previous.feedback.reviews) {{
          const prevFb = DATA.previous.feedback.reviews.find(r => r.run_id === prevRun.id);
          if (prevFb && prevFb.feedback) {{
            html += `<p style="color:#d29922;font-size:13px;margin-top:8px;">Previous feedback: ${{escapeHtml(prevFb.feedback)}}</p>`;
          }}
        }}
        html += `</details>`;
      }}
    }}

    // Feedback textarea
    const existingFb = (DATA.feedback.reviews || []).find(r => r.run_id === run.id);
    html += `<div class="feedback-area"><h4 style="color:#8b949e;margin-bottom:4px;">Feedback</h4>`;
    html += `<textarea id="fb-${{run.id}}" placeholder="Leave feedback (empty = looks good)">${{existingFb ? escapeHtml(existingFb.feedback) : ''}}</textarea>`;
    html += `</div>`;

    html += `</div></div>`;
  }});

  container.innerHTML = html;
}}

function renderBenchmark() {{
  const container = document.getElementById('tab-benchmark');
  const bm = DATA.benchmark;

  if (!bm) {{
    container.innerHTML = '<p style="color:#8b949e;text-align:center;padding:40px;">No benchmark data available. Run aggregate_benchmark.py first.</p>';
    return;
  }}

  let html = '<h2 style="margin-bottom:16px;">Benchmark Results</h2>';

  if (bm.configurations) {{
    html += '<table class="benchmark-table"><thead><tr>';
    html += '<th>Configuration</th><th>Pass Rate</th><th>Time (s)</th><th>Tokens</th><th>Runs</th>';
    html += '</tr></thead><tbody>';

    bm.configurations.forEach(cfg => {{
      const stats = cfg.stats || {{}};
      const pr = stats.pass_rate || {{}};
      const time = stats.time_seconds || {{}};
      const tokens = stats.total_tokens || {{}};
      const prColor = (pr.mean || 0) >= 0.8 ? '#3fb950' : (pr.mean || 0) >= 0.5 ? '#d29922' : '#f85149';
      html += `<tr>`;
      html += `<td style="font-weight:600">${{cfg.name || 'unknown'}}</td>`;
      html += `<td style="color:${{prColor}}">${{((pr.mean || 0) * 100).toFixed(1)}}% \u00b1 ${{((pr.stddev || 0) * 100).toFixed(1)}}%</td>`;
      html += `<td>${{(time.mean || 0).toFixed(1)}}s \u00b1 ${{(time.stddev || 0).toFixed(1)}}s</td>`;
      html += `<td>${{Math.round(tokens.mean || 0)}} \u00b1 ${{Math.round(tokens.stddev || 0)}}</td>`;
      html += `<td>${{cfg.run_count || 0}}</td>`;
      html += `</tr>`;
    }});
    html += '</tbody></table>';
  }}

  if (bm.delta) {{
    html += '<h3 style="margin-top:24px;">Delta (Skill vs Baseline)</h3>';
    html += `<div class="summary">`;
    const d = bm.delta;
    if (d.pass_rate !== undefined) {{
      const color = d.pass_rate > 0 ? '#3fb950' : d.pass_rate < 0 ? '#f85149' : '#8b949e';
      html += `<div class="summary-card"><div class="value" style="color:${{color}}">${{d.pass_rate > 0 ? '+' : ''}}${{(d.pass_rate * 100).toFixed(1)}}%</div><div class="label">Pass Rate Delta</div></div>`;
    }}
    if (d.time_seconds !== undefined) {{
      html += `<div class="summary-card"><div class="value">${{d.time_seconds > 0 ? '+' : ''}}${{d.time_seconds.toFixed(1)}}s</div><div class="label">Time Delta</div></div>`;
    }}
    if (d.total_tokens !== undefined) {{
      html += `<div class="summary-card"><div class="value">${{d.total_tokens > 0 ? '+' : ''}}${{Math.round(d.total_tokens)}}</div><div class="label">Token Delta</div></div>`;
    }}
    html += '</div>';
  }}

  if (bm.observations && bm.observations.length > 0) {{
    html += '<h3 style="margin-top:24px;">Analysis Observations</h3>';
    bm.observations.forEach(obs => {{
      html += `<div style="background:#161b22;border:1px solid #30363d;border-radius:6px;padding:12px;margin:8px 0;font-size:13px;">${{escapeHtml(obs)}}</div>`;
    }});
  }}

  container.innerHTML = html;
}}

function submitFeedback() {{
  const runs = DATA.runs || [];
  const reviews = runs.map(run => ({{
    run_id: run.id,
    feedback: (document.getElementById('fb-' + run.id) || {{}}).value || '',
    timestamp: new Date().toISOString()
  }}));

  const payload = {{ reviews, status: 'complete' }};

  // Try POST to server
  fetch('/api/feedback', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify(payload)
  }}).then(r => {{
    if (r.ok) {{
      alert('Feedback saved!');
    }} else {{
      throw new Error('Server unavailable');
    }}
  }}).catch(() => {{
    // Fallback: download as file
    const blob = new Blob([JSON.stringify(payload, null, 2)], {{ type: 'application/json' }});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'feedback.json';
    a.click();
    URL.revokeObjectURL(url);
    alert('Feedback downloaded as feedback.json -- copy it to the workspace directory.');
  }});
}}

function escapeHtml(text) {{
  const div = document.createElement('div');
  div.textContent = text || '';
  return div.innerHTML;
}}

// Keyboard navigation
document.addEventListener('keydown', (e) => {{
  if (e.target.tagName === 'TEXTAREA') return;
  if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {{
    const cards = document.querySelectorAll('.eval-body');
    const openIdx = Array.from(cards).findIndex(c => c.classList.contains('open'));
    cards.forEach(c => c.classList.remove('open'));
    let next = e.key === 'ArrowRight' ? openIdx + 1 : openIdx - 1;
    next = Math.max(0, Math.min(next, cards.length - 1));
    cards[next].classList.add('open');
    cards[next].scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }}
}});

// Initial render
renderOutputs();
renderBenchmark();
</script>
</body>
</html>"""


def kill_existing_on_port(port: int):
    """Kill any existing process on the target port."""
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True, text=True, timeout=5
        )
        pids = result.stdout.strip().split("\n")
        for pid in pids:
            if pid.strip():
                os.kill(int(pid.strip()), signal.SIGTERM)
    except (subprocess.TimeoutExpired, ProcessLookupError, ValueError):
        pass


class ReviewHandler(BaseHTTPRequestHandler):
    workspace = None
    skill_name = ""
    benchmark_path = None
    previous_workspace = None

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/feedback":
            feedback_path = self.workspace / "feedback.json"
            if feedback_path.exists():
                data = feedback_path.read_text(encoding="utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(data.encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"reviews":[]}')
            return

        # Default: regenerate HTML on every request
        html = generate_html(
            self.workspace,
            self.skill_name,
            self.benchmark_path,
            self.previous_workspace,
        )
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        if self.path == "/api/feedback":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)
                if "reviews" not in data:
                    raise ValueError("Missing 'reviews' field")

                feedback_path = self.workspace / "feedback.json"
                with open(feedback_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status":"saved"}')
            except (json.JSONDecodeError, ValueError) as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(str(e).encode("utf-8"))
            return

        self.send_response(405)
        self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress logs


def main():
    parser = argparse.ArgumentParser(description="Eval viewer for ccbuilder")
    parser.add_argument("workspace", help="Path to iteration workspace directory")
    parser.add_argument("--port", type=int, default=3117, help="Server port (default: 3117)")
    parser.add_argument("--skill-name", default="unknown", help="Skill name for display")
    parser.add_argument("--benchmark", help="Path to benchmark.json")
    parser.add_argument("--previous-workspace", help="Path to previous iteration workspace")
    parser.add_argument("--static", help="Write standalone HTML to this path instead of serving")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    benchmark_path = Path(args.benchmark).resolve() if args.benchmark else None
    previous_workspace = Path(args.previous_workspace).resolve() if args.previous_workspace else None

    if args.static:
        html = generate_html(workspace, args.skill_name, benchmark_path, previous_workspace)
        output_path = Path(args.static)
        output_path.write_text(html, encoding="utf-8")
        print(f"Static HTML written to: {output_path}")
        return

    # Start server
    kill_existing_on_port(args.port)

    ReviewHandler.workspace = workspace
    ReviewHandler.skill_name = args.skill_name
    ReviewHandler.benchmark_path = benchmark_path
    ReviewHandler.previous_workspace = previous_workspace

    server = HTTPServer(("127.0.0.1", args.port), ReviewHandler)
    print(f"Eval viewer running at http://127.0.0.1:{args.port}")
    print(f"Workspace: {workspace}")
    print("Press Ctrl+C to stop")

    # Open browser
    import webbrowser
    webbrowser.open(f"http://127.0.0.1:{args.port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
