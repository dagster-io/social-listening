from dagster_slack import SlackResource
from dagster import (
    Definitions,
    load_assets_from_modules,
    EnvVar,
)
from . import assets
from .sensors.reddit import reddit_comment_sensor, reddit_post_sensor
from .sensors.hackernews import hackernews_sensor
from .resources import Keyword

all_assets = load_assets_from_modules([assets])


defs = Definitions(
    assets=all_assets,
    sensors=[
        reddit_post_sensor,
        reddit_comment_sensor,
        hackernews_sensor,
    ],
    resources={
        "slack": SlackResource(token=EnvVar("SLACK_BOT_TOKEN")),
        "keyword": Keyword(value="dagster"),
    },
)
