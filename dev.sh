if ! heroku apps:info -a itkpi &>/dev/null
	then
	echo "No app 'itkpi' in account. Login to proper account."
	exit 1
fi
heroku git:remote -a itkpi

if [ -e venv ]
	then
	echo "venv already exists. Remove to recreate virtualenv"
	exit 2
fi
virtualenv3 venv

source venv/bin/activate
pip install -r requirements.txt

MAILCHIMP_APIKEY="$(heroku config:get MAILCHIMP_APIKEY)"
echo "MAILCHIMP_API_KEY = '${MAILCHIMP_APIKEY}'" > itkpi/local_settings.py
