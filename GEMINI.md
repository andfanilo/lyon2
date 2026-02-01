# Lyon 2 SISE Tutorials

## Project Overview

This repository contains the source code for the Lyon 2 SISE tutorials documentation site. It covers various topics related to modern data engineering and machine learning operations, including:

*   **MLOps:** Machine Learning Operations.
*   **NoSQL:** Not Only SQL databases.
*   **Spark:** Apache Spark for big data processing.
*   **GenAI:** Generative AI.
*   **Kubernetes:** Container orchestration.

The documentation is built using [MkDocs](https://www.mkdocs.org/) with the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. It also includes utility scripts for generating dummy data (HTTP logs) used in the tutorials.

## Tech Stack

*   **Documentation:** MkDocs, Material for MkDocs
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
*   `site/`: The generated static site (created after running `mkdocs build`).
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
uv run mkdocs serve
```

The site will be available at `http://127.0.0.1:8000/`.

### Building the Site

Build the static site:

```bash
uv run mkdocs build
```

To preview the built site locally:

```bash
cd site/
uv run python -m http.server
```

### Deployment

The site is deployed to GitHub Pages. Due to 2FA requirements, manual deployment via the CLI is often used:

```bash
uv run mkdocs build
uv run mkdocs gh-deploy
```

## Log Generator Utility

The `gen_logs` directory contains a tool to simulate web traffic logs, likely used for Spark or NoSQL tutorials.

*   **Start:** `./gen_logs/start_logs.sh` (Runs the generator in the background and writes to `gen_logs/logs/access.log`)
*   **Stop:** `./gen_logs/stop_logs.sh`
*   **Tail:** `./gen_logs/tail_logs.sh`

## Key Files

*   `mkdocs.yml`: The main configuration file for the MkDocs site.
*   `pyproject.toml`: Project metadata and dependencies.
*   `README.md`: Basic project information and commands.
