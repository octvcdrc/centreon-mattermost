#Author : Cedric Octave (cedric<at>octvcdrc.fr)
#Just type 'python centreon-mattermost-service.py -h' to get some help.

import requests, argparse

##################################
## Command arguments definition ##
##################################
parser = argparse.ArgumentParser(description='Process centreon notifications to send them to a mattermost webhook.')

parser.add_argument('--url',
					required=True,
					help='Mattermost webhook url',
					)

parser.add_argument('--channel',
					required=True,
					help='Channel to output to',
					)

parser.add_argument('--icon-url',
					help='The url of the bot avatar. Defaults to the webhook icon.',
					default=False,
					)

parser.add_argument('--username',
					help='The username of the bot, defaults to "Centreon"',
					default='Centreon',
					)

parser.add_argument('--verify-ssl',
					help='Default to true. Set it to True if you use self signed certificates, or like to live dangerously.',
					default=True,
					)

parser.add_argument('--notification-type',
					choices=['PROBLEM',
						'RECOVERY',
						'ACKNOWLEDGEMENT',
						'FLAPPINGSTART',
						'FLAPPINGSTOP',
						'FLAPPINGDISABLED',
						'DOWNTIMESTART',
						'DOWNTIMEEND',
						'DOWNTIMECANCELLED',
					],
					required=True,
					help='The output of $NOTIFICATIONTYPE$',
					)

parser.add_argument('--hostname',
					required=True,
					help='The output of $HOSTNAME$',
					)

parser.add_argument('--service-desc',
					required=True,
					help='The output of $SERVICEDESC$',
					)

parser.add_argument('--service-output',
					required=True,
					help='The output of $SERVICEOUTPUT$',
					)

parser.add_argument('--service-state',
					choices=['OK',
						'WARNING',
						'CRITICAL',
						'UNKNOWN',
					],
					required=True,
					help='The output of $SERVICESTATE$',
					)

parser.add_argument('--service-ack-author',
					default=False,
					help='The output of $SERVICEACKAUTHOR$, just used in acknowlegements.',
					)

parser.add_argument('--notification-comment',
					default=False,
					help='The output of $NOTIFICATIONCOMMENT$, used in acknowlegements, downtime start/end and custom.',
					)

args = parser.parse_args()

##################################
# Message generation and sending #
##################################

# Protip : you can change the emojis below.
ok_icon = ':white_check_mark:'
warning_icon = ':warning:'
info_icon = ':information_source:'
ack_icon = ':ballot_box_with_check:'

payload={'channel': args.channel,
	'username': args.username,
}

if (args.icon_url != False):
	payload['icon_url'] = args.icon_url

if (args.notification_type == 'PROBLEM'):
	payload['text'] = '# ' + warning_icon + '\nService ' + args.service_desc + ' on host ' + args.hostname + ' is ' + args.service_state + '\nStatus: `' + args.service_output + '`'

if (args.notification_type == 'RECOVERY'):
	payload['text'] = '# ' + ok_icon + '\nService ' + args.service_desc + ' on host ' + args.hostname + ' seems fine now.\nStatus: `' + args.service_output + '`'

if (args.notification_type == 'ACKNOWLEDGEMENT'):
	payload['text'] = '# ' + ack_icon + '\nService ' + args.service_desc + ' on host ' + args.hostname + ' has been acknowleged by ' + args.service_ack_author + '.'
	if (args.notification_comment != False):
		payload['text'] += '\nComment: `' + args.notification_comment + '`'

if (args.notification_type == 'FLAPPINGSTART'):
	payload['text'] = '# ' + warning_icon + '\n' + args.service_desc + ' on host ' + args.hostname + ' has started flapping.'

if (args.notification_type == 'FLAPPINGSTOP'):
	payload['text'] = '# ' + ok_icon + '\nService ' + args.service_desc + ' on host ' + args.hostname + ' has stopped flapping.'

if (args.notification_type == 'FLAPPINGDISABLED'):
	payload['text'] = '# ' + info_icon + '\nFlapping of service ' + args.service_desc + ' on host ' + args.hostname + ' is disabled.'

if (args.notification_type == 'DOWNTIMESTART'):
	payload['text'] = '# ' + info_icon + '\nService ' + args.service_desc + ' on host ' + args.hostname + ' is now in downtime.'
	if (args.notification_comment != False):
		payload['text'] += '\nComment: `' + args.notification_comment + '`'

if (args.notification_type == 'DOWNTIMEEND'):
	payload['text'] = '# ' + info_icon + '\nService ' + args.service_desc + ' on host ' + args.hostname + ' is no longer in downtime.'
	if (args.notification_comment != False):
		payload['text'] += '\nComment: `' + args.notification_comment + '`'

if (args.notification_type == 'DOWNTIMECANCELLED'):
	payload['text'] = '# ' + info_icon + '\nDowntime of service ' + args.service_desc + ' on host ' + args.hostname + ' has been canceled.'

# Not sure if this is a valid notification type but it appears in the Centreon documentation so let's handle it.
# Appears here : https://documentation.centreon.com/docs/centreon-engine/en/1.7/user/configuration/basics/standard_macros.html#notificationcomment
if (args.notification_type == 'CUSTOM'):
	payload['text'] = '## ' + info_icon + '\nService ' + args.service_desc + ' on host ' + args.hostname + ' just received a custom notification.'
	if (args.notification_comment != False):
		payload['text'] += '\nComment: `' + args.notification_comment + '`'

r = requests.post(args.url, json=payload, verify=args.verify_ssl)
