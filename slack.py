#!/usr/bin/env python3
try:
    import os
    from slackclient import SlackClient
except Exception as e:
    print("EXCEPTION: %s" % e)

def main():
    try:
        # Pull environment variables from Icinga and set some defaults
        service = os.getenv('SERVICEDISPLAYNAME')
        host = os.getenv('HOSTALIAS')
        output = os.getenv('HOSTOUTPUT', os.getenv('SERVICEOUTPUT'))
        state = os.getenv('HOSTSTATE', os.getenv('SERVICESTATE'))

        # If this is a service state instead of just a host, set the format to HOST/SERVICE
        if service != "":
            host += "/" + service
        
        # Set the color for Slack message attachments
        color = "#FF0000"
        if state == 'UP' or state == 'OK':
            color = "#00FF00"
        elif state == 'WARNING':
            color = "#0000FF"

        # HOST is STATE: \n MESSAGE
        msg = "%s is %s: \n %s" % (host, state, output)
        attachment = '[{"fallback": "%s", "color": "%s", "text": "%s"}]' % (msg, color, msg)

        # Post the message to Slack
        slack_message(attachment)

    except Exception as e:
        print("Error " + e)

def slack_message(msg):
    # Get the Slack Key from Icinga Env Variable
    slack_key = os.getenv("ICINGA_SLACK_KEY")
    client = SlackClient(slack_key)

    # Post a Slack message with an attachment, as a bot user
    resp = client.api_call("chat.postMessage", channel="#home-automation", attachments=msg, as_user=True)

    # Print the Slack response for debugging purposes
    print (resp)

main()
