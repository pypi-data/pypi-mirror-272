async def test_contract_context(hub):
    await hub.pop.sub.add(
        pypath=["tests.mods.contract_ctx"],
        subname="mods",
        contracts_pypath=["tests.contracts"],
    )
    assert await hub.mods.ctx.test() == "contract executed"
    # Multiple calls have the same outcome
    assert await hub.mods.ctx.test() == "contract executed"


async def test_contract_context_update_call(hub):
    # if a pre modifies args, make sure they persist when called via 'call' function
    await hub.pop.sub.add(
        pypath=["tests.mods.contract_ctx"],
        subname="mods",
        contracts_pypath=["tests.contracts"],
    )
    assert await hub.mods.ctx_update.test_call(True) == "contract executed"
    # Multiple calls have the same outcome
    assert await hub.mods.ctx_update.test_call(True) == "contract executed"


async def test_contract_context_update_direct(hub):
    # if a pre modifies args, make sure they persist when called directly
    await hub.pop.sub.add(
        pypath=["tests.mods.contract_ctx"],
        subname="mods",
        contracts_pypath=["tests.contracts"],
    )
    assert await hub.mods.ctx_update.test_direct(True) is False
    assert await hub.mods.ctx_update.test_direct(True) is False
