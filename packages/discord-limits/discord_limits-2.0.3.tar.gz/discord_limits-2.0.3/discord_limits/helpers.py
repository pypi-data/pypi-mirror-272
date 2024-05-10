import datetime
from .errors import OldMessageID


def snowflake_time(id: int, /) -> datetime.datetime:
    """Returns the creation time of the given snowflake.

    .. versionchanged:: 2.0
        The ``id`` parameter is now positional-only.

    Parameters
    -----------
    id: :class:`int`
        The snowflake ID.

    Returns
    --------
    :class:`datetime.datetime`
        An aware datetime in UTC representing the creation time of the snowflake.
    """
    timestamp = ((id >> 22) + 1420070400000) / 1000
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)


def check_bulk_delete_ids(message_ids: list[int]):
    """Check if the messages are younger than 14 days.

    Parameters
    ----------
    message_ids : list[int]
        A list of message IDs to check.

    Raises
    ------
    ValueError
        If the message ID is older than 14 days.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    for message in message_ids:
        if (now - snowflake_time(int(message))) >= datetime.timedelta(days=14):
            raise OldMessageID(
                message,
                f"The message ID {message} is older than 14 days and cannot be deleted in bulk.",
            )
