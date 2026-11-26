# TD 6 - Analytics Engineering with dbt

## Objectives

- [ ] Create a dbt project on DuckDB with uv
- [ ] Load seeds and declare a raw log file as a source
- [ ] Parse raw logs into staging models
- [ ] Build a daily revenue mart
- [ ] Test and document your models

## Prerequisites

Make sure you have the following installed:

- [uv](https://docs.astral.sh/uv/), see [TD 0](prerequisites.md)
- [Visual Studio Code](https://code.visualstudio.com/) (highly recommended with the "dbt Power User" extension)
- A terminal
- A clone of this tutorials repository, <https://github.com/andfanilo/lyon2>: the TD uses its `gen_logs` script to generate data

---

## 1. Setup & Installation

In this tutorial, we will build a "Modern Data Stack" locally. instead of a cloud warehouse like Snowflake or BigQuery, we will use **DuckDB**, an in-process SQL OLAP database that is fast and easy to set up.

### a. Project Initialization

We will create a specific directory for our analytics project to keep it separate from the documentation site.

!!! note "Exercise - Environment Setup"
    - Create a new folder named `dbt_project` at the root of your repository (sibling to `docs`, `gen_logs`, etc.).
    - Open your terminal in this new folder.
    - Initialize a new uv project:
        ```bash
        uv init --app --no-package --no-workspace --vcs none --python 3.12
        ```
        - Without `--no-workspace`, uv adds `dbt_project` to the repository's own `pyproject.toml`, the one that builds this documentation site.
    - Add dbt for DuckDB to the project:
        ```bash
        uv add dbt-duckdb
        ```
    - Run every dbt command through `uv run`, from `dbt_project` or any folder inside it. Check that it works with `uv run dbt --version`.

### b. dbt Initialization

dbt (data build tool) comes with a CLI to scaffold projects.

!!! note "Exercise - Create the dbt project"
    - Run the initialization command:
        ```bash
        uv run dbt init ecommerce_analytics
        ```
    - The wizard will ask you for configuration:
        - **Database**: Select `duckdb`.
        - **plugins**: Press Enter.
        - **threads**: 1 or 4.
        - **path**: Type `dbt.duckdb` (This is crucial to save your data to a file!).
    - Once finished, you will have a `ecommerce_analytics` folder. Open it in VS Code.

### c. The profiles.yml

You might wonder: *Where is the database connection defined?*
By default, `dbt init` creates a global configuration file in your home directory (`~/.dbt/profiles.yml`).

For this project to be self-contained, we will create a local configuration.

!!! note "Exercise - Local Configuration"
    - Inside your `ecommerce_analytics` folder, create a file named `profiles.yml`.
    - Paste the following content:

    ```yaml
    ecommerce_analytics:
      target: dev
      outputs:
        dev:
          type: duckdb
          path: 'dbt.duckdb'
          extensions: 
            - httpfs
            - parquet
    ```
    - **Crucial**: From now on, when you run dbt commands, you must tell dbt to look for the profile in the current directory.
    - You have two options:
  
        1.  Add the flag: `uv run dbt debug --profiles-dir .`
        2.  (Recommended) Set an environment variable in your terminal:

            === "Git Bash / WSL / macOS / Linux"

                ```bash
                export DBT_PROFILES_DIR=.
                ```

            === "PowerShell"

                ```powershell
                $env:DBT_PROFILES_DIR="."
                ```
    
    - Run `uv run dbt debug` to confirm the connection works.

    *Note: The `extensions` list ensures DuckDB can read remote files and parquet, which is useful for advanced features.*

## 2. The Scenario: E-Commerce Traffic

You are the Analytics Engineer for a growing e-commerce site. The backend team has provided you with:

1.  **Raw Server Logs**: A messy stream of HTTP requests containing valuable user behavior data.
2.  **Product Catalog**: Static JSON files describing the products and categories.

Your goal is to turn this mess into a clean "Daily Revenue" report.

### a. Generate Data

We will use the repository's existing tools to generate our raw data.

!!! note "Exercise - Data Generation"
    - Go back to the `dbt_project` folder.
    - Generate 50,000 log lines with the repository's `gen_logs` script:
        ```bash
        uv run python ../gen_logs/lib/genhttplogs.py --count 50000 > ecommerce_analytics/access.log
        ```
        *Note: The script works from any folder. Without `--count`, it streams one line per second until you stop it with Ctrl+C.*
    - Copy the dimension data into your dbt project's `seeds` folder.
        - Source: `gen_logs/data/products.json`, `departments.json`, `categories.json`
        - Destination: `dbt_project/ecommerce_analytics/seeds/`

    Your folder structure should look like this:
    ```
    dbt_project/
    └── ecommerce_analytics/
        ├── access.log
        ├── dbt_project.yml
        ├── seeds/
        │   ├── products.json
        │   ├── departments.json
        │   └── categories.json
        ├── models/
        └── ...
    ```

## 3. Ingestion (Bronze Layer)

In the "Modern Data Stack", we often follow the ELT (Extract, Load, Transform) pattern. We load raw data first, then transform it in place.

### a. Seeds (Dimensions)

dbt "Seeds" are perfect for static data like our product catalogs.

!!! note "Exercise - Loading Seeds"
    - In your terminal (inside `ecommerce_analytics`), run:
        ```bash
        uv run dbt seed
        ```
    - dbt will automatically infer schemas from the JSON files and create tables in your DuckDB database (by default, a file named `dbt.duckdb` will appear).
    - You can verify the data using the DuckDB CLI or by installing the `duckdb` python package and querying it, but trusting dbt is usually enough!

### b. External Sources (Facts)

The `access.log` is a raw text file. We don't want to manually insert it. DuckDB is amazing because it can query files directly.

!!! note "Exercise - Configure the Source"
    - Create a new file `models/sources.yml`.
    - We will define a source that points to our local file.
    
    ```yaml
    version: 2

    sources:
      - name: raw_data
        schema: main
        tables:
          - name: access_logs
            description: "Raw server logs from the webserver"
            meta:
              external_location: "read_text('access.log')"
    ```
    
    *Note: `read_text` is a DuckDB function that reads a file line by line into a single column named `content`.*

## 4. Transformation (Silver Layer)

Now that our data is "defined", we need to parse it. The logs are currently just unstructured text strings.

### a. Staging Models

We will create a "staging" model to clean up the raw data. This is where we apply Regex to extract columns.

!!! note "Exercise - Parsing Logs"
    - Create a new file `models/staging/stg_access_logs.sql`.
    - We need to extract the **IP**, **Timestamp**, **URL**, and **Status Code**.
    - Copy the following SQL (DuckDB dialect):

    ```sql
    with source as (
        select * from {{ source('raw_data', 'access_logs') }}
    ),

    parsed as (
        select
            -- DuckDB regex extraction
            regexp_extract(content, '^(\S+)', 1) as ip_address,
            strptime(regexp_extract(content, '\[(.*?)\]', 1), '%d/%b/%Y:%H:%M:%S %z') as log_timestamp,
            regexp_extract(content, '"GET (.*?) HTTP', 1) as url,
            cast(regexp_extract(content, 'HTTP/1.1" (\d{3})', 1) as int) as status_code
        from source
    )

    select * from parsed
    ```
    - Run `uv run dbt run` to build this model.
    - Inspect the view/table created in DuckDB (or use `uv run dbt show --select stg_access_logs`).

### b. Feature Extraction

We have a `url` column, but we need business context. The URLs look like `/product/105` or `/add_to_cart/105`.

!!! danger "Challenge - Extracting Context"
    - Modify `models/staging/stg_access_logs.sql`.
    - Add logic to extract:
        - `product_id`: The number at the end of `/product/...` or `/add_to_cart/...` URLs.
        - `action`: The type of action (e.g., 'view_product', 'add_to_cart', 'checkout').
    
    *Hint: You can use `case when` statements with `LIKE` operators or more regex.*
    
    <details>
    <summary>Click for Solution</summary>
    
    ```sql
    select
        ip_address,
        log_timestamp,
        status_code,
        url,
        -- Extract Product ID if present
        case 
            when url like '/product/%' then split_part(url, '/', 3)
            when url like '/add_to_cart/%' then split_part(url, '/', 3)
            else null 
        end as product_id,
        -- Label the action
        case
            when url like '/product/%' then 'view_product'
            when url like '/add_to_cart/%' then 'add_to_cart'
            when url = '/checkout' then 'checkout'
            else 'browse'
        end as action
    from parsed
    where status_code = 200 -- We only care about successful requests
    ```
    </details>

## 5. Business Logic (Gold Layer)

Now that we have clean events, we can join them with our dimension tables to calculate business metrics.

### a. Potential Revenue Mart

We want to know how much money is being "added to cart" each day.

!!! note "Exercise - Daily Revenue Mart"
    - Create a new file `models/marts/mart_daily_revenue.sql`.
    - We need to:
        1. Select from `stg_access_logs`.
        2. Filter for `add_to_cart` actions.
        3. Join with the `products` seed to get the price.
        4. Group by day.

    ```sql
    with logs as (
        select * from {{ ref('stg_access_logs') }}
    ),
    
    products as (
        select * from {{ ref('products') }}
    )
    
    select
        -- Truncate timestamp to day
        date_trunc('day', logs.log_timestamp) as report_date,
        sum(products.product_price) as potential_revenue,
        count(*) as items_added
    from logs
    join products on cast(logs.product_id as int) = products.product_id
    where logs.action = 'add_to_cart'
    group by 1
    order by 1 desc
    ```
    - Run `uv run dbt run`.

## 6. Quality & Documentation

A huge advantage of dbt is that documentation and testing are code, living right next to your SQL.

### a. Testing

!!! note "Exercise - Add Tests"
    - Open `models/schema.yml` (create it if it doesn't exist).
    - Add tests to ensure our data assumptions hold true.

    ```yaml
    version: 2

    models:
      - name: stg_access_logs
        columns:
          - name: log_timestamp
            tests:
              - not_null
          - name: action
            tests:
              - accepted_values:
                  values: ['view_product', 'add_to_cart', 'checkout', 'browse']

      - name: mart_daily_revenue
        columns:
          - name: report_date
            tests:
              - unique
              - not_null
    ```
    - Run `uv run dbt test`. If everything is correct, all tests should pass (green).

### b. Documentation

!!! note "Exercise - Generate Documentation"
    - Run the following command:
        ```bash
        uv run dbt docs generate
        ```
    - Then launch the local documentation server:
        ```bash
        uv run dbt docs serve
        ```
    - A browser tab will open. Explore the **Lineage Graph** (bottom right icon). You will see the full flow of your data from `access.log` to `mart_daily_revenue`.

---

## Recap

!!! success "Check that you can explain your neighbor each point of the checklist below"
    - [x] Create a dbt project on DuckDB with uv
    - [x] Load seeds and declare a raw log file as a source
    - [x] Parse raw logs into staging models
    - [x] Build a daily revenue mart
    - [x] Test and document your models

You have built a complete ELT pipeline locally!

1.  **Extract**: Read raw text logs.
2.  **Load**: DuckDB accessed them directly.
3.  **Transform**: Parsed Regex, joined with JSON seeds, and aggregated revenue.



