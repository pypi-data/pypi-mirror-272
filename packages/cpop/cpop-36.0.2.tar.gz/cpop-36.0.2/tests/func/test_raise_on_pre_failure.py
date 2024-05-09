import cpop.exc
import pytest


@pytest.fixture(scope="function")
async def hub(hub):
    await hub.pop.sub.add(dyne_name="cn")
    yield hub


async def test_pre_fail_sync(hub):
    with pytest.raises(
        cpop.exc.PreContractFailed,
        match=r"Pre contract '\w+' failed for function '\w+'",
    ):
        await hub.cn.test.func1()


async def test_pre_fail_async(hub):
    with pytest.raises(
        cpop.exc.PreContractFailed,
        match=r"Pre contract '\w+' failed for function '\w+'",
    ):
        await hub.cn.test.afunc1()


async def test_pre_fail_gen(hub):
    with pytest.raises(
        cpop.exc.PreContractFailed,
        match=r"Pre contract '\w+' failed for function '\w+'",
    ):
        async for _ in hub.cn.test.gen1():
            ...
