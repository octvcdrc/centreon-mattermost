About

Get notifications from centreon to mattermost.
Voilà.

Usage

Clone this repo.

Host notification command
/usr/local/bin/python PATH/centreon-mattermost/centreon-mattermost-host.py --url="MATTERMOST_WEBHOOK_URL" --channel="CHANNEL" --hostname="$HOSTNAME$" --host-output="$HOSTOUTPUT$" --host-state="$HOSTSTATE$" --notification-type="$NOTIFICATIONTYPE$" --host-ack-author="$HOSTACKAUTHOR$" --notification-comment="$NOTIFICATIONCOMMENT$"

Service notification command
/usr/local/bin/python PATH/centreon-mattermost/centreon-mattermost-service.py --url="MATTERMOST_WEBHOOK_URL" --channel="CHANNEL" --hostname="$HOSTNAME$" -- service-desc="$SERVICEDESC" --service-output="$SERVICEOUTPUT$" --service-state="$SERVICESTATE$" --notification-type="$NOTIFICATIONTYPE$" --service-ack-author="$SERVICEACKAUTHOR$" --notification-comment="$NOTIFICATIONCOMMENT$"
