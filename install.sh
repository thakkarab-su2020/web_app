#! /bin/bash
cd /home/ubuntu/
pwd
ls -al
python3 -m venv ./venv
source venv/bin/activate
pip3 install -r myproject/requirements.txt
sudo chown ubuntu:www-data -R /home/ubuntu/myproject/
sudo chmod 775 -R /home/ubuntu/myproject/
source export.sh
python3 myproject/manage.py migrate
source export.sh
python3 myproject/manage.py collectstatic -y
sudo cp myproject/deploy/gunicorn.service /etc/systemd/system/
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo cp myproject/deploy/myproject /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
sudo nginx -t && sudo systemctl restart nginx