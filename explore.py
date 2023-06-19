# Connect via Slack's API and explore the public channels owners
# Pre-requisites: Python 3.6+, slack_sdk -> pip3 install slack_sdk
# Usage: set SLACK_API_TOKEN env variable and run `python3 explore.py`
# Slack OAuth Scopes needed: channels:read, users:read, channels:history, groups:read
import os
import time

from slack_sdk import WebClient

CHANNEL_TYPES = ["public_channel"]


def get_channel_creator(channel_id, web_client):
    time.sleep(2)
    channel_info = web_client.conversations_info(channel=channel_id)
    if not channel_info["ok"]:
        print(f"Failed to retrieve channel info for channel: {channel_id}")
        return None

    # There are several ways to get the 'name' of the creator
    # 'real_name' should be the one to tag for a message, let's see
    # See https://api.slack.com/methods/users.info for more info
    creator_info = web_client.users_info(user=channel_info["channel"]["creator"])
    if not creator_info["ok"]:
        print(f"Failed to retrieve creator info for channel: {channel_id}")
        return None

    real_name = creator_info.get("user").get("real_name")
    name = creator_info.get("user").get("name")
    return real_name, name


def main():
    access_token = os.getenv("SLACK_API_TOKEN")
    assert (
        access_token
    ), "SLACK_API_TOKEN is not set. Check your SLACK_API_TOKEN env variable."

    web_client = WebClient(token=access_token)
    channels = []
    continue_paging = True
    cursor = None
    while(continue_paging):
        print(f"[DEBUG] paging cursor: {cursor}")
        time.sleep(2)
        response = web_client.conversations_list(types=CHANNEL_TYPES, cursor=cursor)
        if not response.get("ok"):
            return response.get("error")
        cursor = response.get("response_metadata").get("next_cursor")
        if not cursor or cursor == "":
            continue_paging = False
        channels_page = response.get("channels")
        if channels_page:
            channels.extend(channels_page)

    for channel in channels:
        print(f"[DEBUG] Querying {channel['name']}")
        creator_name, creator_real_name = get_channel_creator(channel["id"], web_client)
        if creator_name:
            print(f"{channel['name']}, {creator_name}, {creator_real_name}")

if __name__ == "__main__":
    main()
