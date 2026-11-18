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

*   **Python environments:** `prerequisites.md` teaches `uv venv` + `uv pip` as a bridge, then the project workflow (`uv init`, `uv add`, `uv run`), then `uvx` and `uv tool install`. Other TDs use the project workflow only.
*   **`uv init` flags:** always `--app --no-package`, because recent uv versions default to a `src/` package. Add `--vcs none` for projects nested in a student folder (MLOps services, MCP server). Add `--no-workspace` for projects created inside this repository (dbt): without it, uv adds them to the root `pyproject.toml` workspace.
*   **One uv project per Docker image:** MLOps `client/`, `server/`, GenAI `mcp-server/`, `agent/`. GenAI exercises share one `genai-td` project.
*   **Dockerfiles:** `FROM python:3.12-slim`, `COPY --from=ghcr.io/astral-sh/uv:<pinned> /uv /uvx /bin/`, copy `pyproject.toml uv.lock`, `uv sync --locked --no-install-project`, copy the code, `CMD ["uv", "run", ...]`. Each project has a `.dockerignore` with `.venv`. Keep the uv version identical across pages.
*   **Shells:** Git Bash is the default. Use content tabs (`=== "Git Bash"`, `=== "PowerShell"`, `=== "WSL / macOS / Linux"`) only where commands differ. In Git Bash, `docker run -v` with a Linux path needs `MSYS_NO_PATHCONV=1`.
*   **Pending:** `prerequisites.md` step 4 (`uvx jupyter lab` on the cloned pyspark-tutorial) is temporary until the pyspark-tutorial environment setup (nbgrader, VS Code) is decided.

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
