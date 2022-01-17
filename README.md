# Drone Delivery

There is a major new technology that is destined to be a disruptive force in the field of transportation: **the drone**. Just as the mobile phone allowed developing countries to leapfrog older technologies for personal communication, the drone has the potential to leapfrog traditional transportation infrastructure.

Useful drone functions include delivery of small items that are (urgently) needed in locations with difficult access.

## Features
- Create Drone
- Create Medications
- Create Medication Packages
- Create Package Shipments
- Update battery status every 1 minute

## Tech

**Drone Delivery** uses a number of projects to work properly:

- [Python] - https://www.python.org
- [Django] - https://docs.djangoproject.com
- [Django REST framework] - https://www.django-rest-framework.org/
- [Redis] - https://redis.io/
- [Celery] - https://docs.celeryproject.org
- [django-simple-history] - https://django-simple-history.readthedocs.io/en/latest/index.html

And of course **Drone Delivery** itself is open source with a [public](https://github.com/josueisaihs/drones) on GitHub.

## Installation

Drone Delivery requires to run:
| Dependency | Version |
| ------ | ------ |
|[Celery](	https://github.com/celery/celery/)|5.2.3|
|[Django](https://docs.djangoproject.com)|4.0.1|
|[Django Filter](https://github.com/carltongibson/django-filter/tree/main)|21.1|
|[Django REST Framework](https://www.django-rest-framework.org/)|3.13.1|
|[Django Simple History](https://github.com/jazzband/django-simple-history/blob/master/docs/index.rst)|3.0.0|
|[Python](https://docs.python.org/3.8/)| 3.8.8 |
|[Redis](https://github.com/redis/redis-py)|4.1.0|

### Install
---
#### Linux and Mac
Clone github repository:
```sh
git clone https://github.com/josueisaihs/drones
```
Create virtual environment and activate it:
```sh
python3 -m venv env/
source env/bin/activate
```
Install dependencies:
```sh
cd src
pip install -r requirements.txt
```
Create the database file and create the models in the database:
```sh
cd drones
./manage.py migrate
```
#### Load data to test the app
Create data tot test the app:
```sh
./manage.py create_data --all
```
(optional) Added custom commands to add and remove data for testing the app.
The options of the create command are:
```sh
./manage.py create_data [--all] [--drone] [--medications] [--package]
optional arguments:
--drone         Create 10 drones with random data 
--medication    Create medications with random data
--package       Create packets with random data
--all           Create all the above data
```
The options of the remove command are:
```sh
./manage.py clean_data [--all] [--drone] [--medications] [--package] [--delivery]
optional arguments:
--drone         Remove drones
--medication    Remove medications
--package       Remove packets
--delivery      Remove delivery packages
--all           Remove all data
```
### Settings
Must set the following fields in the ``settings.py``:
```python
DRONE_DELIVERY_CONFIG = {
    "MAX_WEIGHT": 500.0,
    "LOW_BATTERY": 25.0,
    "BATTERY_STATUS_UPDATE_TIME": 1,
}
```

| Key | Description |
| ------ | ------ |
|MAX_WEIGHT | Maximum capacity that supports a drone |
| LOW_BATTERY | Indicates value to decide if the battery is low |
| BATTERY_STATUS_UPDATE_TIME | Time in minutes to run the drone battery level update task |

#### Run Server 
Finally, run the following to launch the local server
```sh
./manage.py runserver
```
#### Redis
First download [Redis](https://download.redis.io/releases/redis-6.2.6.tar.gz) and read the ``README`` file.
Open the downloaded folder in the another terminal and simply run:
```sh
make
```
After building Redis, it is a good idea to test it using:
```sh
make test
```
To run Redis with the default configuration, just type:
```sh
cd src
./redis-server
```
You can use redis-cli to play with Redis. Start a redis-server instance,
then in another terminal try the following:
```sh
cd src
./redis-cli
redis> ping
PONG
redis>quit
```
#### Celery
Open a new instance of the terminal in the project's containing folder to initialize celery:
```sh
source env/bin/activate
cd src/drones
celery -A drones worker -l info
```
And open an another instance of the terminal in the project's containing folder and run the following:
```sh
source env/bin/activate
cd src/drones
celery -A drones beat -l info
```