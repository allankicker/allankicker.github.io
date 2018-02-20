Light chat app 

### Installation (python2.7 and pip required)

sudo apt-get install rabbitmq-server virtualenv

sudo service rabbitmq-server start

virtualenv lightchat

. lightchat/bin/activate

pip install pika

### Start app

Start a first client, inside source dir: 

```
. lightchat/bin/activate
python client.py
``` 

Start a second client in a second terminal, the same way.

Now the 2 clients are connected and each one receive messages from the other one.

### Limitation 

Disconnected clients will not receive messages sent while they were offline
All clients are connected to the same channel
