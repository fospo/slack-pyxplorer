# Slack Explorer

## Slack App creation & installation
This is a Slack App so in order to use the script you need to first create and app and install it inside the proper Slack Workspace as follows:

1. Visit the Slack API website.
2. Sign in to your Slack workspace.
3. Navigate to the Slack App Directory and click on the "Create New App" button.
4. Provide a name for your app and select the workspace where you want to install it. Click on the "Create App" button.
5. In the left sidebar, under "Features," click on "OAuth & Permissions."
6. Under the "Scopes" section, add the following OAuth scopes:

```
channels:read
users:read
channels:history
groups:read
```

7. Scroll up and click on the "Install App to Workspace" button to install the app to your workspace.

After installation, you will see the "OAuth Access Token" under the "OAuth Tokens & Redirect URLs" section. That is the token that you need to use, so just

``` bash
export SLACK_API_TOKEN=<your-api-token>
```

and then run

```bash
python3 explore.py
```

## Functionality
The script performs the following tasks:

1. Retrieves the Slack API token from the environment variable SLACK_API_TOKEN.
2. Initializes the Slack Web Client using the API token.
3. Retrieves a list of public channels using the conversations_list method of the Slack API.
4. For each channel, retrieves information about the channel's creator using the conversations_info and users_info methods.
5. Prints the name and real name of the channel's creator to the console.
