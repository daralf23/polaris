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


class ContextPlugin:
    name = "context_test"

    async def run(self, context, config):
        assert context.state is not None
        assert context.scheduler is not None
        assert context.dispatcher is not None
        assert context.logger is not None
        assert context.job_name == "test_job"

        return Event(
            title="Context",
            message="Context Test",
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


@pytest.mark.asyncio
async def test_scheduler_builds_plugin_context(
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
        ContextPlugin(),
        {},
        "test_job",
    )

    dispatcher.send.assert_awaited_once()
