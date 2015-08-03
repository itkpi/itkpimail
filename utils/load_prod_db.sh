set -x

rm -f db.sqlite3
heroku run  'python manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission --exclude=admin.LogEntry; sleep 5' > data.json
sed -i.bak '/^[^\[]/d' data.json
python manage.py migrate
python manage.py loaddata data.json
rm -f data.json
