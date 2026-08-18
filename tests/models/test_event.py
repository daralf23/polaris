from polaris.models.event import Event, EventLevel


def test_event_defaults():
    event = Event(
        title="Test Title",
        message="Test Hello World",
    )

    assert event.title == "Test Title"
    assert event.message == "Test Hello World"
    assert event.level == EventLevel.INFO
    assert event.source is None
    assert event.timestamp is not None
