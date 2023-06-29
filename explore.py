# Connect via Slack's API and explore the public channels owners
# Pre-requisites: Python 3.6+, slack_sdk -> pip3 install slack_sdk
# Usage: set SLACK_API_TOKEN env variable and run `python3 explore.py`
# Slack OAuth Scopes needed: channels:read, users:read, channels:history, groups:read
# Using sleep and pagination to avoid rate limiting, see https://api.slack.com/docs/rate-limits
import os
import time
from slack_sdk import WebClient

CHANNEL_TYPES = ["public_channel"]
CHANNELS_PER_PAGE = 50
SLEEP_TIME = 2


def get_channel_creator(channel_id, web_client):
    channel_info = web_client.conversations_info(channel=channel_id)
    if not channel_info["ok"]:
        print(f"Failed to retrieve channel info for channel: {channel_id}")
        return None

    creator_info = web_client.users_info(user=channel_info["channel"]["creator"])
    if not creator_info["ok"]:
        print(f"Failed to retrieve creator info for channel: {channel_id}")
        return None

    return creator_info["user"]["name"], creator_info["user"]["real_name"]


def process_channel(channel, web_client):
    creator_name, creator_real_name = get_channel_creator(channel["id"], web_client)
    if creator_name:
        print(f"{channel['name']}, {creator_name}, {creator_real_name}")


def main():
    access_token = os.getenv("SLACK_API_TOKEN")
    assert access_token, "SLACK_API_TOKEN is not set. Check your SLACK_API_TOKEN env variable."

    web_client = WebClient(token=access_token)
    cursor = None

    while True:
        time.sleep(SLEEP_TIME)
        print(f"Processing cursor: {cursor}")
        channel_list_response = web_client.conversations_list(types=CHANNEL_TYPES, limit=CHANNELS_PER_PAGE, cursor=cursor)
        if not channel_list_response.get("ok"):
            print(channel_list_response.get("error"))
            break

        channels = channel_list_response.get("channels")
        [process_channel(channel, web_client) for channel in channels]

        cursor = channel_list_response.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    exit(0)


if __name__ == "__main__":
    main()
