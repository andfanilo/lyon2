## Installation

```
pip install mkdocs-material
```

## Dev

```
mkdocs serve
```

## Build

```
mkdocs build
cd site/
python -m http.server
```

## Deploy 

Because of 2FA, deploy with:

```
mkdocs build
mkdocs gh-deploy
```