This script will publish timeline and favorited tweets to a fluentd sink.

Set the following environment variables from a twitter dev account:

'APP_KEY'
'APP_SECRET'
'OAUTH_TOKEN'
'OAUTH_TOKEN_SECRET'

# Setup a virtualenv
$ virtualenv env

# Install requirements
$ env/bin/pip install -r requirements.txt

# Run the main script
$ env/bin/python publish_script.
