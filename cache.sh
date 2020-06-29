#! /bin/bash
cd /home/ubuntu/
DIR=/home/ubuntu/myproject
if [ -d "$DIR" ]; then
    sudo rm -rf myproject/
    sudo systemctl daemon-reload
    sudo systemctl restart gunicorn
    sudo nginx -t && sudo systemctl restart nginx
else 
    echo "$DIR does not exist."
fi
