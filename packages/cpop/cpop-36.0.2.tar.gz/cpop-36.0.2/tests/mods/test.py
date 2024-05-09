import os

from cpop.scanner import scan

__virtualname__ = "test"
__contracts__ = "test"
__func_alias__ = {"ping_": "ping"}


async def ping_(hub):
    return {}


async def demo(hub):
    return False


async def this(hub):
    return await hub._.ping()


async def fqn(hub):
    return await hub.mods.test.ping()


async def module_level_non_aliased_ping_call(hub):
    return await ping_()  # pylint: disable=no-value-for-parameter


async def module_level_non_aliased_ping_call_fw_hub(hub):
    return await ping_(hub)


async def attr(hub):
    return True


attr.bar = True
attr.func = True


async def call_scan(hub):
    # If scan has been loaded as a Contract, the call below will throw a TypeError because
    # we'll also pass hub
    scan([os.path.dirname(__file__)])
    return True


async def double_underscore(hub):
    assert hub.__ is hub.mods
    assert hub.___ is hub
    assert hub.______ is hub
