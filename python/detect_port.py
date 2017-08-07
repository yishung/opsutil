import os
import subprocess
import sys

# (MUST) read the host addresses from environment , split by ','
hosts = os.getenv('hosts','')

# (MUST) read the port from environment , eg:mongo port = 27017
port = os.getenv('port',0)

# (OPTIONAL) set nc timeout
timeout = os.getenv('timeout',30)


def sendToSlack(msg):
    from slackclient import SlackClient
    print('sendToSlack:\n' + msg)

    # (MUST) slack api token
    token = os.getenv('slack_token','')

    # (OPTIONAL) target channel
    channel = os.getenv('channel','#general')

    if not token:
        print("cannot find slack_token!!")
        sys.exit(1)

    slack_client = SlackClient(token)
    rt = slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text= msg,
        username='detect_port'
    )

    if not rt.get('ok',False):
        print('sendToSlack failed!!')
        sys.exit(1)


if hosts and port:
    msg = ''
    for host in hosts.split(','):
        cmd = 'nc -zv -w {} {} {}'.format(timeout, host, port)
        print('cmd:' + str(cmd))
        exit_code = subprocess.call(cmd, shell=True)
        print('exit_code:' + str(exit_code))

        if (1 == exit_code):
            if not msg:
                msg = 'failed cmd'
            msg += ('\n' + cmd)

    if msg:
        sendToSlack(msg)


