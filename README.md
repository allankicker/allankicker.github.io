Light chat app 

### Installation (python2.7 and pip required)

sudo apt-get install rabbitmq-server virtualenv

sudo service rabbitmq-server start

virtualenv lightchat

pip install pika

. lightchat/bin/activate

### Start app

Start a first client, inside source dir: 

``` python client.py ``` 

Start a second client in another terminal

Now the 2 clients are connected and each one receive messages from the others

### Limitation 

Disconnected clients will not receive messages sent while they were offline
