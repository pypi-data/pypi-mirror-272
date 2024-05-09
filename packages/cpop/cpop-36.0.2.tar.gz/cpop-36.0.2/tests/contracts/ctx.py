"""
Contract Context
"""

__virtualname__ = "ctx"


async def pre(hub, ctx):
    """ """
    assert "injected_data" not in ctx.cache
    ctx.cache["injected_data"] = 1


async def call(hub, ctx):
    """ """
    if "injected_data" not in ctx.cache:
        raise AssertionError(
            "'injected_data' was not found in contract call 'ctx.cache'"
        )
    ctx.cache["injected_data"] += 1
    return "contract executed"


async def post_ping(hub, ctx):
    """ """
    if "injected_data" not in ctx.cache:
        raise AssertionError(
            "'injected_data' was not found in contract post 'ctx.cache'"
        )
    assert ctx.cache["injected_data"] == 2
    return ctx.ret
