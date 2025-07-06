# This is the line to add to crontab file (crontab -e command)
# It will upload files to stanford via ftp at 5:05pm LOCAL TIME every day.
# It should be a bit after 00:00 UTC time, so adjust for your local time zone.
# This change of the crontab is only required if supersid.cfg configures automatic_upload = no

# m h  dom mon dow   command
5 17 * * * python3 /home/steve/supersid/src/ftp_outgoing.py -c /home/steve/supersid/Config/supersid.cfg
