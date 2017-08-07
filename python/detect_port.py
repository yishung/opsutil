import os
import subprocess

# (MUST) read the host addresses from environment , split by ','
hosts = os.getenv('hosts','')

# (MUST) read the port from environment , eg:mongo port = 27017
port = os.getenv('port',0)

# (OPTIONAL) set nc timeout
timeout = os.getenv('timeout',30)


def sendToSlack(msg):
    from slacker import Slacker
    token = os.getenv('slack_token',"")
    if token:
        slack = Slacker(token)
        slack.chat.post_message('#general', msg)


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

    if not msg:
        sendToSlack(msg)


