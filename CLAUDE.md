# CLAUDE.md

This file guides Claude Code (claude.ai/code) when it works in this repository.

# Lyon 2 SISE Tutorials

## Project Overview

This repository contains the source code for the Lyon 2 SISE tutorials documentation site. It covers various topics related to modern data engineering and machine learning operations, including:

*   **MLOps:** Machine Learning Operations.
*   **NoSQL:** Not Only SQL databases.
*   **Spark:** Apache Spark for big data processing.
*   **GenAI:** Generative AI.
*   **Kubernetes:** Container orchestration.

[Zensical](https://zensical.org/) builds the documentation from `mkdocs.yml`, with the `modern` theme variant. `docs/stylesheets/extra.css` sets the teal primary and accent colours. In `modern`, the primary colour styles text links only, and the accent colour styles the current page in the sidebar. The header stays white. The repository also includes utility scripts for generating dummy data (HTTP logs) used in the tutorials.

## Tech Stack

*   **Documentation:** Zensical (reads `mkdocs.yml`)
*   **Language:** Python (>=3.11)
*   **Package Manager:** uv
*   **CI/CD:** GitHub Actions (for deployment)

## Directory Structure

*   `docs/`: Contains the Markdown source files for the documentation.
    *   `images/`: Images used in the documentation.
    *   `stylesheets/`: Custom CSS files.
*   `gen_logs/`: A utility tool to generate fake HTTP access logs.
    *   `lib/genhttplogs.py`: The main Python script for log generation.
    *   `data/`: JSON data sources (products, departments, categories) for the log generator.
    *   `start_logs.sh`, `stop_logs.sh`, `tail_logs.sh`: Shell scripts to manage the log generation process.
*   `site/`: The generated static site (created after running `zensical build`).
*   `data/`: Miscellaneous data files (CSV, ZIP) used in tutorials.
*   `.github/workflows/`: CI/CD configuration files.

## Development Workflow

### Prerequisites

Ensure you have `uv` installed.

### Installation

Install dependencies:

```bash
uv sync
```

### Local Development

Start the local development server:

```bash
uv run zensical serve
```

The site will be available at `http://127.0.0.1:8000/`.

### Building the Site

Build the static site:

```bash
uv run zensical build --strict
```

`--strict` fails the build on a broken link or anchor. CI runs it too.

To preview the built site locally:

```bash
cd site/
uv run python -m http.server
```

### Deployment

A push to `master` runs `.github/workflows/ci.yml`, which builds the site and publishes it with the GitHub Pages actions. To redeploy without a push, run the workflow from the **Actions** tab. Zensical has no `gh-deploy` command.

Zensical does not support MkDocs `hooks` or arbitrary MkDocs plugins. Check the [supported plugins](https://zensical.org/docs/compatibility/mkdocs/plugins/) before adding one.

## Tutorial Conventions

The tutorials teach [uv](https://docs.astral.sh/uv/). Do not reintroduce conda, Anaconda or `pip install -r requirements.txt`.

*   **Python environments:** All TDs, `prerequisites.md` included, use the project workflow only (`uv init`, `uv add`, `uv run`, `uv sync`). `prerequisites.md` also teaches `uvx` and `uv tool install`. Don't teach `uv venv`, `uv pip` or activating `.venv`.
*   **`uv init` flags:** always `--app --no-package`, because recent uv versions default to a `src/` package. Add `--vcs none` for projects nested in a student folder (MLOps services, MCP server). Add `--no-workspace` for projects created inside this repository (dbt): without it, uv adds them to the root `pyproject.toml` workspace.
*   **One uv project per Docker image:** MLOps `client/`, `server/`, GenAI `mcp-server/`, `agent/`. GenAI exercises share one `genai-td` project.
*   **Dockerfiles:** `FROM python:3.12-slim`, `COPY --from=ghcr.io/astral-sh/uv:<pinned> /uv /uvx /bin/`, copy `pyproject.toml uv.lock`, `uv sync --locked --no-install-project`, copy the code, `CMD ["uv", "run", ...]`. Each project has a `.dockerignore` with `.venv`. Keep the uv version identical across pages.
*   **Shells:** Git Bash is the default. Use content tabs (`=== "Git Bash"`, `=== "PowerShell"`, `=== "WSL / macOS / Linux"`) only where commands differ. In Git Bash, `docker run -v` with a Linux path needs `MSYS_NO_PATHCONV=1`.
*   **pyspark-tutorial setup:** `spark.md` holds the JupyterLab and VS Code setup (Java, `JAVA_HOME`, uv interpreter and kernel selection). The notebooks set `PYSPARK_PYTHON` to `sys.executable` in their Spark setup cell, and the repo ships a `.env` file for VS Code, so students never set `PYSPARK_PYTHON` by hand. `prerequisites.md` step 6 links to `spark.md` instead of repeating it.
*   **lyon2-docker-demo:** `prerequisites.md` has students clone https://github.com/andfanilo/lyon2-docker-demo into `C:\workspace` and run it with uv, Docker and an AI coding assistant (tabs: GitHub Copilot CLI, Gemini CLI, Claude Code). Keep its commands in sync with that repository's README.

### Exercise style

To review a whole TD against these rules, use the `lab-tutorial-review` skill.

*   **Page structure:** `# TD N - Title`, a short intro, `## Objectives` (a checklist of actions), `## Prerequisites` (tools, and links to TD 0 or earlier TDs), the numbered sections, then `## Recap`. The Recap repeats the Objectives in a `!!! success` block.
*   **Grading:** TD 0 is not graded. In graded TDs, everything before `## Recap` is graded. Graded TDs (MLOps, Spark, NoSQL so far) have a `## 💯 Send me your work` (a Unicode emoji, not a `:shortcode:`: the right sidebar drops shortcode images) section right after the Recap: what to zip (without `.venv`), the file name `<td>-<lastname>-<firstname>.zip`, and "send it to your teacher by email". Don't write an email address. `## Bonus challenges` comes after it and is not graded.
*   **Setup pages for external labs:** Spark and NoSQL set up a graded lab that lives in another repository (`pyspark-tutorial`, `lyon2-nosql`). They end with a `## N. Start the graded lab` section after "Check your setup", not with a link at the top.
*   **lyon2-nosql:** a uv project with a `docker-compose.yml` that starts Redis, MongoDB and OrientDB. `pyorient` is old and prints `SyntaxWarning` on first import, and it needs `orientdb:2.2`. Keep `nosql.md` in sync with that repository's README.

*   **Admonitions:** `!!! note "Exercise - <task>"` is only for exercises. `extra.css` renders notes as white cards. Keep explanations as plain prose between exercises, outside any admonition.
*   **Section endings:** a `!!! question` block with 2 or 3 "why" questions. Ungraded TDs, such as TD 0, add a collapsed `??? tip "Going further"` block with optional tasks for fast students.
*   **Challenges:** a Challenge block is a harder task, with less guidance than an exercise. The admonition type sets the difficulty: `!!! warning "Challenge - …"` is medium, `!!! danger "Challenge - …"` is hard. Challenges before the Recap are graded, as a bonus.
*   **Hints:** when a step gives only the goal, put the commands in a collapsed `??? tip "Hint"` inside the exercise.
*   **Self-checks:** each exercise tells students what success looks like at least once, for example "You should see `All checks passed!`".
*   **Predict, then run:** before a command with a surprising result, ask "Before you run it, predict…".
*   **Fail first:** show the error a tool prevents before you teach the tool, for example `python app.py` before `uv run app.py`.
*   **One new idea per step.** Split an exercise that brings in many new flags.
*   **No time estimates**, and no sentences that announce what the page layout already shows.
*   **Run before you write.** Run every command and observe every output you claim. Before you use a package to show a missing dependency, check that the project does not already pull it in. Streamlit already brings in `rich`.
*   **Markdown trap:** leave a blank line before `---`. Text directly above `---` becomes a heading.

## Log Generator Utility

The `gen_logs` directory contains a tool to simulate web traffic logs, likely used for Spark or NoSQL tutorials.

*   **Fixed count:** `uv run python gen_logs/lib/genhttplogs.py --count 1000 > out.log` writes 1000 lines and exits. Works from any folder.
*   **Start:** `./gen_logs/start_logs.sh` (Runs the generator in the background and writes to `gen_logs/logs/access.log`)
*   **Stop:** `./gen_logs/stop_logs.sh`
*   **Tail:** `./gen_logs/tail_logs.sh`

## Key Files

*   `mkdocs.yml`: The site configuration, in MkDocs format, read by Zensical.
*   `pyproject.toml`: Project metadata and dependencies.
*   `README.md`: Basic project information and commands.
