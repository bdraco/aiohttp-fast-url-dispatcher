import asyncio
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from aiohttp import web
from yarl import URL

from aiohttp_fast_url_dispatcher import FastUrlDispatcher, attach_fast_url_dispatcher


def test_attach_fast_url_dispatcher() -> None:
    """Test attaching the fast url dispatcher to an app."""
    dispatcher = FastUrlDispatcher()
    app = web.Application()
    attach_fast_url_dispatcher(app, dispatcher)
    assert isinstance(app._router, FastUrlDispatcher)
    app = web.Application(router=dispatcher)
    assert isinstance(app._router, FastUrlDispatcher)


@pytest.mark.asyncio
async def test_dispatch(tmp_path: Path) -> None:
    """Test the FastUrlDispatcher."""
    dispatcher = FastUrlDispatcher()
    index_path = tmp_path.joinpath("index.html")
    index_path.write_text("Hello World!")
    dispatcher.add_static("/static", tmp_path, show_index=True)
    payload = MagicMock()
    protocol = MagicMock()

    url = URL("/static/index.html")
    message = MagicMock(url=url, method="GET")
    request = web.Request(
        message,
        payload,
        protocol=protocol,
        host="example.com",
        task=MagicMock(),
        loop=asyncio.get_running_loop(),
        payload_writer=MagicMock(),
    )
    assert request.rel_url == url
    match_info = await dispatcher.resolve(request)
    assert match_info is not None
    assert match_info.route.resource.canonical == "/static"

    url = URL("/static/index.html")
    message = MagicMock(url=url, method="WRONG")
    request = web.Request(
        message,
        payload,
        protocol=protocol,
        host="example.com",
        task=MagicMock(),
        loop=asyncio.get_running_loop(),
        payload_writer=MagicMock(),
    )
    assert request.rel_url == url
    match_info = await dispatcher.resolve(request)
    assert match_info is not None
    assert match_info.route.status == 405

    url = URL("/not_registered")
    message = MagicMock(url=url, method="GET")
    request = web.Request(
        message,
        payload,
        protocol=protocol,
        host="example.com",
        task=MagicMock(),
        loop=asyncio.get_running_loop(),
        payload_writer=MagicMock(),
    )
    assert request.rel_url == url
    match_info = await dispatcher.resolve(request)
    assert match_info is not None
    assert match_info.route.status == 404


@pytest.mark.asyncio
async def test_template_at_slash() -> None:
    """Test the FastUrlDispatcher with a template at /."""
    dispatcher = FastUrlDispatcher()

    async def handler():
        return web.Response(text="Hello World!")

    dispatcher.add_get(r"/{any}", handler)
    payload = MagicMock()
    protocol = MagicMock()

    url = URL("/wildcard")
    message = MagicMock(url=url, method="GET")
    request = web.Request(
        message,
        payload,
        protocol=protocol,
        host="example.com",
        task=MagicMock(),
        loop=asyncio.get_running_loop(),
        payload_writer=MagicMock(),
    )
    assert request.rel_url == url
    match_info = await dispatcher.resolve(request)
    assert match_info is not None
    assert match_info.route.resource.canonical == "/{any}"

    url = URL("/not/registered")
    message = MagicMock(url=url, method="GET")
    request = web.Request(
        message,
        payload,
        protocol=protocol,
        host="example.com",
        task=MagicMock(),
        loop=asyncio.get_running_loop(),
        payload_writer=MagicMock(),
    )
    assert request.rel_url == url
    match_info = await dispatcher.resolve(request)
    assert match_info is not None
    assert match_info.route.status == 404
