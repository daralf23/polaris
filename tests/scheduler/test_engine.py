import pytest

from polaris.models.event import Event
from polaris.scheduler.engine import SchedulerEngine


class FakePlugin:
    name = "fake"

    async def run(self, context, config):
        return Event(
            title="Test",
            message="Scheduler Test",
        )


@pytest.mark.asyncio
async def test_scheduler_runs_plugin(
    plugin_context,
    config_loader,
    logger,
    state,
    dispatcher,
):
    engine = SchedulerEngine(
        config_loader=config_loader,
        logger=logger,
        dispatcher=dispatcher,
        state=state,
    )

    await engine._run_plugin(
        FakePlugin(),
        {},
    )

    dispatcher.send.assert_awaited_once()
