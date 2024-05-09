repeats = 10000


async def test_direct(hub):
    await hub.pop.sub.add(pypath=["tests.mods"])
    for i in range(repeats):
        await hub.mods.test.ping()


async def test_contract(hub):
    await hub.pop.sub.add(pypath=["tests.cmods"])
    for i in range(repeats):
        await hub.cmods.ctest.cping()


async def test_via_fqn(hub):
    await hub.pop.sub.add(pypath=["tests.mods"])
    for i in range(repeats):
        await hub.mods.test.fqn()
