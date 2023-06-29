from dagster import (
    sensor,
    AssetSelection,
    SensorResult,
    SkipReason,
    RunRequest,
    RunConfig,
    SensorEvaluationContext,
)
import os
import requests


from ..resources import Keyword
from ..assets.reddit import reddit_mention, RedditAssetConfig


@sensor(
    asset_selection=AssetSelection.assets(reddit_mention),
    # longer interval to allow enough time pulling data from external apis
    minimum_interval_seconds=60,
)
def reddit_post_sensor(
    context: SensorEvaluationContext,
    keyword: Keyword,
):
    """Polls the Reddit API for new mentions.

    When we find one, add it to the set of partitions and run the processing pipeline on it.
    """

    latest_tracked_mention = context.cursor

    # We abstract this one to be "take a keyword" Resource so it's easy to change it "globally" for all sensors
    keyword_to_listen = keyword.get_value()

    # Call Reddit API to fetch recent mentions since latest tracked record.
    headers = _auth_and_get_headers()
    # The first time we turn on the sensor (i.e. cursor will be empty), we will fetch the latest
    # 25 posts, to avoid unexpected large numbers of runs. This means that you might need to
    # manually backfill earlier mentions if you want the full history.
    response = requests.get(
        # Confusingly, after means further back in time, whereas before means more recently in time.
        f"https://oauth.reddit.com/search/?q={keyword_to_listen}&sort=new"
        + (f"&before={latest_tracked_mention}" if latest_tracked_mention else ""),
        headers=headers,
    )

    children = response.json()["data"]["children"]
    if not children:
        return SkipReason("No new mentions")

    new_mentions = []

    for item in children[::-1]:
        new_mentions.append(
            RedditAssetConfig(
                fullname=item["data"]["name"],
                url=item["data"]["url"],
                type="post",
                slack_channel="#social-feed-test",
            )
        )

    return SensorResult(
        cursor=new_mentions[-1].fullname,
        run_requests=[
            RunRequest(
                run_key=item.fullname,
                run_config=RunConfig(ops={"reddit_mention": item}),
            )
            for item in new_mentions
        ],
    )


@sensor(
    asset_selection=AssetSelection.assets(reddit_mention),
    # longer interval to allow enough time pulling data from external apis
    minimum_interval_seconds=60,
)
def reddit_comment_sensor(
    context: SensorEvaluationContext,
    keyword: Keyword,
):
    """Polls the Reddit API for new mentions.

    When we find one, add it to the set of partitions and run the processing pipeline on it.
    """

    latest_tracked_mention = context.cursor

    # We abstract this one to be "take a keyword" Resource so it's easy to change it "globally" for all sensors
    keyword_to_listen = keyword.get_value()

    # Call Reddit API to fetch recent mentions since latest tracked record.
    headers = _auth_and_get_headers()

    # The first time we turn on the sensor (i.e. cursor will be empty), we will fetch the latest
    # 25 posts, to avoid unexpected large numbers of runs. This means that you might need to
    # manually backfill earlier mentions if you want the full history.
    response = requests.get(
        # Confusingly, after means further back in time, whereas before means more recently in time.
        f"https://oauth.reddit.com/search/?q={keyword_to_listen}&sort=new&type=comment"
        + (f"&before={latest_tracked_mention}" if latest_tracked_mention else ""),
        headers=headers,
    )

    children = response.json()["data"]["children"]
    if not children:
        return SkipReason("No new mentions")

    new_mentions = []

    for item in children[::-1]:
        new_mentions.append(
            RedditAssetConfig(
                fullname=item["data"]["name"],
                url=item["data"]["url"],
                type="comment",
                slack_channel="#social-feed-test",
            )
        )

    return SensorResult(
        cursor=new_mentions[-1].fullname,
        run_requests=[
            RunRequest(
                run_key=item.fullname,
                run_config=RunConfig(ops={"reddit_mention": item}),
            )
            for item in new_mentions
        ],
    )


def _auth_and_get_headers():
    auth = requests.auth.HTTPBasicAuth(
        os.environ["REDDIT_PERSONAL_USE_SCRIPT"], os.environ["REDDIT_SECRET"]
    )

    # here we pass our login method (password), username, and password
    data = {
        "grant_type": "password",
        "username": os.environ["REDDIT_USERNAME"],
        "password": os.environ["REDDIT_PASSWORD"],
    }

    # setup our header info, which gives reddit a brief description of our app
    headers = {"User-Agent": "test-dagster-bot-0/0.0.1"}
    # send our request for an OAuth token
    res = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )
    # convert response to JSON and pull access_token value
    TOKEN = res.json()["access_token"]

    if not res.ok:
        res.raise_for_status()

    # add authorization to our headers dictionary
    headers = {**headers, **{"Authorization": f"bearer {TOKEN}"}}

    return headers
