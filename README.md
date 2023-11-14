# aiohttp-fast-url-dispatcher

<p align="center">
  <a href="https://github.com/bdraco/aiohttp-fast-url-dispatcher/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/bdraco/aiohttp-fast-url-dispatcher/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://aiohttp-fast-url-dispatcher.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/aiohttp-fast-url-dispatcher.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">
  </a>
  <a href="https://codecov.io/gh/bdraco/aiohttp-fast-url-dispatcher">
    <img src="https://img.shields.io/codecov/c/github/bdraco/aiohttp-fast-url-dispatcher.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">
  </a>
  <a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/aiohttp-fast-url-dispatcher/">
    <img src="https://img.shields.io/pypi/v/aiohttp-fast-url-dispatcher.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/aiohttp-fast-url-dispatcher.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/aiohttp-fast-url-dispatcher.svg?style=flat-square" alt="License">
</p>

---

**Documentation**: <a href="https://aiohttp-fast-url-dispatcher.readthedocs.io" target="_blank">https://aiohttp-fast-url-dispatcher.readthedocs.io </a>

**Source Code**: <a href="https://github.com/bdraco/aiohttp-fast-url-dispatcher" target="_blank">https://github.com/bdraco/aiohttp-fast-url-dispatcher </a>

---

A faster URL dispatcher for aiohttp

The default `UrlDispatcher` implementation does a linear search every which can have a significant [TimeComplexity](https://wiki.python.org/moin/TimeComplexity) when dispatching urls when there are a lot of routes. `FastUrlDispatcher` keeps an index of the urls which allows for fast dispatch.

## Installation

Install this via pip (or your favourite package manager):

`pip install aiohttp-fast-url-dispatcher`

## Usage

Attach to a `web.Application` before any resources are registered.

```python
dispatcher = FastUrlDispatcher()
app = web.Application()
attach_fast_url_dispatcher(app, dispatcher)
```

Create with a new `web.Application`

```python
dispatcher = FastUrlDispatcher()
app = web.Application(router=dispatcher)
```

### Caveats

If you have multiple handlers that resolve to the same URL, this module will always prefer the static name over a dynamic name. For example:

```python
app.router.add_get(r"/second/{user}/info", handler)
app.router.add_get("/second/bob/info", handler)
```

`"/second/bob/info"` will always be matched before `r"/second/{user}/info"`

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- markdownlint-disable -->
<!-- markdownlint-enable -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
