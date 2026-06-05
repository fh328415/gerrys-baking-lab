#!/usr/bin/env python3
"""
generate_index.py
─────────────────
Scans all Markdown files in logs/session-*.md, extracts their YAML
frontmatter, and writes a fully styled HTML table to docs/index.html.

Called by: .github/workflows/deploy-pages.yml
Uses:      Python standard library only — no pip install required.

Environment variables:
  GITHUB_REPOSITORY  e.g. "gerry/gerrys-baking-lab"
                     Set automatically by the GitHub Actions workflow.
                     Falls back to "owner/gerrys-baking-lab" when run locally.
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone


# ── Frontmatter parser ────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> dict:
    """
    Extract the YAML frontmatter block from a Markdown file and return
    it as a plain dictionary of { key: value } strings.

    We use a hand-rolled parser instead of a YAML library so this script
    works with zero dependencies. It handles simple key: value pairs only —
    which is all our session logs use.

    Example input:
        ---
        session_id: "2026-04-10-001"
        date: "2026-04-10"
        baker: "María González"
        ---

    Returns:
        {"session_id": "2026-04-10-001", "date": "2026-04-10", ...}
    """
    if not text.startswith("---"):
        return {}

    try:
        end_index = text.index("---", 3)
    except ValueError:
        return {}

    frontmatter_block = text[3:end_index]
    result = {}

    for line in frontmatter_block.splitlines():
        # Match lines of the form:  key: some value
        match = re.match(r"^(\w+)\s*:\s*(.+)", line.strip())
        if match:
            key = match.group(1).strip()
            # Strip surrounding quotes if present
            value = match.group(2).strip().strip('"').strip("'")
            result[key] = value

    return result


# ── URL builder ───────────────────────────────────────────────────────────────

def build_github_url(relative_path: str, repo: str, branch: str = "main") -> str:
    """
    Convert a repo-relative path (e.g. logs/session-2026-04-10.md) to a
    GitHub "blob" URL that renders the file nicely in the GitHub UI.

    Example output:
        https://github.com/gerry/gerrys-baking-lab/blob/main/logs/session-2026-04-10.md
    """
    clean_path = relative_path.replace("\\", "/").lstrip("./")
    return f"https://github.com/{repo}/blob/{branch}/{clean_path}"


# ── HTML builder ─────────────────────────────────────────────────────────────

def build_html(rows_html: str, repo: str, generated_at: str) -> str:
    """Return the complete HTML page as a string."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Gerry's Baking Lab — Session Index</title>
  <style>
    /* ── Reset & base ── */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #fdf6ec;
      color: #2d2d2d;
      line-height: 1.6;
      padding: 2.5rem 1rem;
    }}

    /* ── Layout ── */
    .container {{ max-width: 980px; margin: 0 auto; }}

    /* ── Header ── */
    header {{ margin-bottom: 2.5rem; }}

    header h1 {{
      font-size: 2rem;
      color: #7b3f00;
      letter-spacing: -0.5px;
    }}

    header p {{ color: #666; margin-top: 0.35rem; font-size: 1rem; }}

    .badge {{
      display: inline-block;
      margin-top: 0.75rem;
      background: #7b3f00;
      color: #fff;
      font-size: 0.75rem;
      padding: 0.2rem 0.65rem;
      border-radius: 999px;
      letter-spacing: 0.4px;
      font-weight: 500;
    }}

    /* ── Table ── */
    .table-wrap {{
      overflow-x: auto;
      border-radius: 10px;
      box-shadow: 0 2px 14px rgba(0, 0, 0, 0.08);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      background: #fff;
    }}

    thead tr {{ background: #7b3f00; color: #fff; }}

    thead th {{
      padding: 0.8rem 1.1rem;
      text-align: left;
      font-weight: 600;
      font-size: 0.8125rem;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      white-space: nowrap;
    }}

    tbody tr {{ border-bottom: 1px solid #f0e6d6; }}
    tbody tr:last-child {{ border-bottom: none; }}
    tbody tr:hover {{ background: #fdf0e0; transition: background 0.1s; }}

    td {{
      padding: 0.8rem 1.1rem;
      font-size: 0.9375rem;
      vertical-align: top;
    }}

    td.date   {{ white-space: nowrap; color: #555; font-variant-numeric: tabular-nums; }}
    td.baker  {{ white-space: nowrap; font-weight: 500; }}
    td.hyp    {{ color: #444; font-style: italic; }}

    td.link a {{
      color: #b85c00;
      text-decoration: none;
      font-weight: 500;
      white-space: nowrap;
    }}
    td.link a:hover {{ text-decoration: underline; }}

    /* ── Footer ── */
    footer {{
      margin-top: 2rem;
      font-size: 0.8125rem;
      color: #aaa;
      text-align: center;
    }}
    footer a {{ color: #b85c00; text-decoration: none; }}
    footer a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <div class="container">

    <header>
      <h1>🍪 Gerry's Baking Lab</h1>
      <p>A scientific record of chocolate chip cookie experiments.</p>
      <span class="badge">Powered by GitHub Actions</span>
    </header>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Baker</th>
            <th>Hypothesis</th>
            <th>Log</th>
          </tr>
        </thead>
        <tbody>
{rows_html}
        </tbody>
      </table>
    </div>

    <footer>
      <p>
        Auto-generated by
        <a href="https://github.com/{repo}/actions" target="_blank" rel="noopener">GitHub Actions</a>
        &mdash; last updated {generated_at}
      </p>
    </footer>

  </div>
</body>
</html>"""


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    # Locate the repository root (one directory above scripts/)
    repo_root = Path(__file__).resolve().parent.parent
    logs_dir  = repo_root / "logs"
    docs_dir  = repo_root / "docs"
    out_file  = docs_dir / "index.html"

    # GITHUB_REPOSITORY is injected by the workflow (owner/repo-name).
    # When running locally it falls back to a safe placeholder.
    github_repo = os.environ.get("GITHUB_REPOSITORY", "owner/gerrys-baking-lab")

    # Collect all session log files, sorted chronologically by filename
    log_files = sorted(logs_dir.glob("session-*.md"))

    if not log_files:
        print("⚠️  No session log files found in logs/. Writing empty table.")

    # Build one <tr> per session log
    rows = []
    for log_path in log_files:
        text = log_path.read_text(encoding="utf-8")
        fm   = parse_frontmatter(text)

        rel_path   = log_path.relative_to(repo_root).as_posix()
        github_url = build_github_url(rel_path, github_repo)

        date       = fm.get("date",       log_path.stem)
        baker      = fm.get("baker",      "Unknown")
        hypothesis = fm.get("hypothesis", "—")

        rows.append(
            f'          <tr>\n'
            f'            <td class="date">{date}</td>\n'
            f'            <td class="baker">{baker}</td>\n'
            f'            <td class="hyp">{hypothesis}</td>\n'
            f'            <td class="link"><a href="{github_url}" target="_blank" rel="noopener">View Log →</a></td>\n'
            f'          </tr>'
        )

    rows_html     = "\n".join(rows) if rows else \
                    '          <tr><td colspan="4">No session logs found.</td></tr>'
    generated_at  = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Write output
    docs_dir.mkdir(exist_ok=True)
    out_file.write_text(build_html(rows_html, github_repo, generated_at), encoding="utf-8")

    print(f"✅  docs/index.html written — {len(rows)} session(s) listed.")


if __name__ == "__main__":
    main()
