from nitterbot.bot import init
from nitterbot.notifylistener import NotifyListener
from mastodon.errors import MastodonNetworkError


def main():
    listener = NotifyListener()
    mastodon = init()
    # Mastodon.py currently does not support websocket based, multiplexed streams,
    # but might in the future.
    # https://mastodonpy.readthedocs.io/en/stable/10_streaming.html
    # mastodon.stream_user(listener, run_async=True)
    mastodon.status_post(
        status="New deploy or recovering from crash. Ready for posts!",
        visibility="private",
    )
    try:
        mastodon.stream_user(listener)
    except MastodonNetworkError as err:
        print("Network error, reinitializing", err)
        main()  # this needs real refactoring to have proper retries forever, should we re-use the client or listener?


main()
