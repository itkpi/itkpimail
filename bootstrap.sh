apt-get install -y --force-yes python3-setuptools libpq-dev python3-dev git
easy_install3 pip
pip install virtualenv

cd ~
virtualenv venv
source venv/bin/activate
pip install -r /vagrant/requirements.txt

cd /vagrant
python manage.py migrate
python manage.py loaddata local_data.json
python manage.py runserver 0.0.0.0:5000

echo "cd /vagrant" >> /home/vagrant/.profile
echo "source venv/bin/activate" >> /home/vagrant/.profile
