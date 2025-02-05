## Installation

```
uv sync
```

## Dev

```
uv run mkdocs serve
```

## Build

```
uv run mkdocs build
cd site/
uv run python -m http.server
```

## Deploy 

Because of 2FA, deploy with:

```
uv run mkdocs build
uv run mkdocs gh-deploy
```

## Resources

* https://www.polleverywhere.com/home
* https://app.mural.co/t/lyon220229782/home
