## Installation

```
uv sync
```

## Dev

```
uv run zensical serve
```

## Build

```
uv run zensical build --strict
cd site/
uv run python -m http.server
```

## Deploy

Push to `master`. The `ci` GitHub Actions workflow builds the site and publishes it to GitHub Pages. To redeploy without a push, run the workflow from the **Actions** tab.

## Resources

* https://www.polleverywhere.com/home
* https://app.mural.co/t/lyon220229782/home
