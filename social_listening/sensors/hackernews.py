import requests

from dagster import (
    sensor,
    AssetSelection,
    SensorEvaluationContext,
    RunRequest,
    RunConfig,
)

from ..resources import Keyword
from ..assets.hackernews import hackernews_mention, HNAssetConfig


@sensor(
    asset_selection=AssetSelection.assets(hackernews_mention),
    # shorter interval to avoid processing too many entries within a single tick.
    minimum_interval_seconds=15,
)
def hackernews_sensor(
    context: SensorEvaluationContext,
    keyword: Keyword,
):
    latest_tracked_id = int(context.cursor) if context.cursor else None
    response = requests.get("https://hacker-news.firebaseio.com/v0/maxitem.json")

    max_id = response.json()

    # The first time we turn on the sensor, we will set the cursor as the current latest item.
    latest_tracked_id = latest_tracked_id if latest_tracked_id else max_id

    for i in range(latest_tracked_id, max_id + 1):
        response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{i}.json")
        item = response.json()

        # We abstract this one to be "take a keyword" Resource so it's easy to change it "globally" for all sensors
        keyword_to_listen = keyword.get_value()

        text = item.get("title", item.get("text", ""))
        if keyword_to_listen in text.lower():
            yield RunRequest(
                run_key=str(item["id"]),
                run_config=RunConfig(
                    ops={
                        "hackernews_mention": HNAssetConfig(
                            id=str(item["id"]),
                            url=item.get(
                                "url",
                                f"https://news.ycombinator.com/item?id={item['id']}",
                            ),
                            type=item["type"],
                            slack_channel="#social-feed-test",
                        )
                    }
                ),
            )

    context.update_cursor(str(max_id))
