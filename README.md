# 🍪 Gerry's Baking Lab — GitHub Actions Crash Course

A scientific record of chocolate chip cookie experiments — and your introduction to **GitHub Actions**.

---

## What is this repo?

In science, reproducibility depends on rigorous record-keeping. Every experiment gets logged: the hypothesis, the materials, the method, the results, and the conclusions. No lab notebook, no science.

This repository is a **digital lab notebook** for baking experiments. Every session is recorded as a structured Markdown file in the `logs/` folder. But there's a twist: the notebook has an automated quality control system built with **GitHub Actions** — and you're about to interact with it.

---

## Part 1 — Your assignment

**Add your own baking session log to this repository.**

You don't need to understand how the automation works yet. Just follow the steps below and pay attention to what happens. The goal is to *experience* GitHub Actions as a contributor before we talk about how to write one.

---

### Step 1 — Fork and clone the repository

1. Click **Fork** (top-right of this page) to create your own copy of the repo.
2. Clone your fork to your computer:

```bash
git clone https://github.com/YOUR-USERNAME/gerrys-baking-lab.git
cd gerrys-baking-lab
```

---

### Step 2 — Create your session log

Create a new file inside the `logs/` folder. Name it following this convention:

```
logs/session-YYYY-MM-DD.md
```

For example: `logs/session-2026-06-10.md`

Your file **must** include a YAML frontmatter block at the top (between the `---` markers) with these six fields:

```yaml
---
session_id: "2026-06-10-001"
date: "2026-06-10"
baker: "Your Name"
hypothesis: "One sentence describing what you expect and why"
temperature: "375°F / 190°C"
duration: "11 minutes"
---
```

Below the frontmatter, your file **must** contain these four sections (exact spelling matters):

```markdown
## Ingredients

## Procedure

## Observed Results

## Conclusions
```

Fill each section with your own experiment. Look at the existing files in `logs/` for examples — `session-2026-05-28.md` is a good reference.

> **No oven required.** You can invent a hypothetical experiment, adapt an existing session, or describe a baking session you've done in the past. The content is the vehicle; the process is the lesson.

---

### Step 3 — Commit your file

Stage and commit your new log file. Your commit message **must** follow this format:

```
<type>: <short description>
```

Allowed types:

| Type    | When to use                                   |
|---------|-----------------------------------------------|
| `log:`  | Submitting a new baking session               |
| `amend:`| Correcting or updating an existing session    |
| `docs:` | Updating README or other documentation        |
| `chore:`| Workflow or configuration maintenance         |

Example:

```bash
git add logs/session-2026-06-10.md
git commit -m "log: add oat flour experiment 2026-06-10"
```

> If your commit message doesn't match the format, the automated check will fail and explain why. That's intentional — fix it and try again.

---

### Step 4 — Open a Pull Request

Push your branch and open a Pull Request against the **original** `gerrys-baking-lab` repository (not your fork):

```bash
git push origin main
```

Then go to your fork on GitHub, click **"Contribute" → "Open pull request"**.

---

### Step 5 — Watch GitHub Actions run

Once you open the PR, look for the **checks** section near the bottom of the PR page. You will see a workflow named **"Validate Pull Request"** running automatically. It will check:

1. ✅ **Commit message format** — does it match `type: description`?
2. ✅ **Exactly one log file added** — is only one file in `logs/` being added?
3. ✅ **Filename convention** — does the filename follow `session-YYYY-MM-DD.md`?
4. ✅ **Log file structure** — are all required frontmatter fields and sections present?

If any check fails, click **"Details"** next to it. Read the error message. Fix the issue in your file, commit, and push again — the checks will re-run automatically.

When all four checks pass, the PR is ready to merge.

---

### Step 6 — Watch the site update

After the instructor merges your PR, observe the **"Deploy Baking Lab Pages"** workflow run automatically. Within ~30 seconds, the lab's public page will have a new row for your session.

The site is published at:

```
https://YOUR-INSTRUCTOR-USERNAME.github.io/gerrys-baking-lab/
```

---

## How this works (the big picture)

```
You open a PR
      │
      ▼
GitHub Actions runs validate-pr.yml
      │
      ├── ❌ A check fails → workflow exits with an error
      │         You fix the issue, push, checks re-run
      │
      └── ✅ All checks pass → PR is ready to merge
                    │
                    ▼
            Instructor merges PR
                    │
                    ▼
         GitHub Actions runs deploy-pages.yml
                    │
                    ▼
         scripts/generate_index.py runs on GitHub's servers
         Reads all logs/*.md files
         Writes a new docs/index.html
         Commits it back to the repo
                    │
                    ▼
         GitHub Pages serves the updated site 🌐
```

---

## Repository structure

```
gerrys-baking-lab/
├── .github/
│   └── workflows/
│       ├── validate-pr.yml     ← runs on every PR (quality control)
│       └── deploy-pages.yml    ← runs on every merge to main (deployment)
├── logs/
│   └── session-YYYY-MM-DD.md  ← one file per baking session
├── docs/
│   └── index.html             ← auto-generated; served by GitHub Pages
├── scripts/
│   └── generate_index.py      ← Python script that builds the HTML table
└── README.md                  ← this file
```

---

## Setting up GitHub Pages (instructor)

1. Go to **Settings → Pages** in your repository.
2. Under **Source**, select **Deploy from a branch**.
3. Choose branch: `main`, folder: `/docs`.
4. Click **Save**.

The site will be live at `https://YOUR-USERNAME.github.io/gerrys-baking-lab/` within a minute.

---

## Glossary

| Term | Definition |
|---|---|
| **Workflow** | An automated process defined in a `.yml` file inside `.github/workflows/`. |
| **Trigger** | The event that causes a workflow to run (e.g. `pull_request`, `push`). |
| **Job** | A group of steps that run together on the same virtual machine. |
| **Step** | A single task inside a job — either a shell command (`run:`) or a pre-built action (`uses:`). |
| **Runner** | The virtual machine GitHub provides to execute your workflow. |
| **Action** | A reusable, pre-built step you can reference with `uses:` (e.g. `actions/checkout@v4`). |
| **GITHUB_TOKEN** | An automatic credential GitHub injects into every workflow run. Used for read/write access to the repo. |
| **Context expression** | A `${{ ... }}` placeholder that GitHub fills in at runtime (e.g. `${{ github.repository }}`). |
