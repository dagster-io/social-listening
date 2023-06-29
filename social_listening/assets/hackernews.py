from dagster import asset, Config
from dagster_slack import SlackResource


class HNAssetConfig(Config):
    id: str
    url: str
    type: str
    slack_channel: str


@asset
def hackernews_mention(config: HNAssetConfig, slack: SlackResource):
    """
    Parse a HackerNews record and send notification when needed.

    When proper Slack resource is supplied, we send the Reddit link to Slack. In cases
    like backfills, we swap out the Slack resource so no Slack messages will be sent.
    """
    # Send slack alert
    # NOTE: `slack`` is provided via Resource so in cases like backfills or unit tests,
    # we can supply a mock object to avoid sending slack messages.
    slack.get_client().chat_postMessage(channel=config.slack_channel, text=config.url)
