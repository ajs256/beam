from dotenv import load_dotenv
import os 
import slack_bolt
from slack_sdk.web.client import WebClient


load_dotenv() # Pull env vars from .env.

app = slack_bolt.App(
    token=os.environ.get('SLACK_BOT_TOKEN'),
    signing_secret=os.environ.get('SLACK_SIGNING_SECRET')
)

@app.message()
def message_hello(message):
    # say() sends a message to the channel the event fired in
    # say("Hello world!")
    # TODO rate limit: we can only send ~1 message per sec
    send_to_stream(message)

def send_to_stream(message):
    client: WebClient = app.client
    user = client.users_info(user=message['user'])
    
    if user.get('is_bot'):
        return
    
    name = user['user']['profile']['display_name']
    pfp_url = user['user']['profile']['image_72']
    chan_id = message['channel']
    txt = message['text']
    
    to_send = {
            "blocks": [
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": pfp_url,
                            "alt_text": "User's profile picture"
                        },
                        {
                            "type": "mrkdwn",
                            "text": name + " | <#" + chan_id + ">"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "> " + txt
                    }
                }
            ]
        }
    
    print(to_send)

    
    # Now to finally post it!
    client.chat_postMessage(channel=os.environ.get('STREAM_CHANNEL_ID'), blocks=str(to_send['blocks']), text="New beamed message")
    
    

if __name__ == '__main__':
    app.start(port=int(os.environ.get('PORT', 3000)))
    app.client.chat_postMessage(channel=os.environ.get("STREAM_CHANNEL_ID"), text="I'm alive!")