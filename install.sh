sudo apt-get install curl
sudo apt-get install python3-pip
sudo pip3 install django

python3 manage.py migrate
python3 manage.py createsuperuser
