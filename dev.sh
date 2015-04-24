echo " - Setting up Heroku git remote"

if ! heroku apps:info -a itkpi &>/dev/null
	then
		echo "[WARNING] No app 'itkpi' in account. Login to proper account."
	else
		heroku git:remote -a itkpi
fi

echo " - Setting up virtualenv"

if [ -e venv ]
	then
		echo "[WARNING] venv already exists. Remove to recreate virtualenv"
	else
		virtualenv3 venv
		source venv/bin/activate
		pip install -r requirements.txt
fi

echo " - Setting up MailChimp API Key"
MAILCHIMP_APIKEY="$(heroku config:get MAILCHIMP_APIKEY)"
echo "MAILCHIMP_API_KEY = '${MAILCHIMP_APIKEY}'" > itkpimail/local_settings.py

