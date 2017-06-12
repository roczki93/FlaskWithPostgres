# FlaskWithPostgres

run on Centos 7

sudo yum install epel-release

yum install python-pip python-devel gcc nginx

mkdir flaskapp
cd flaskapp
virtualenv flask
flask/bin/pip install flask
download app.py
chmod a+x app.py
./app.py 
