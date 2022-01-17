# Drone Delivery

There is a major new technology that is destined to be a disruptive force in the field of transportation: **the drone**. Just as the mobile phone allowed developing countries to leapfrog older technologies for personal communication, the drone has the potential to leapfrog traditional transportation infrastructure.

Useful drone functions include delivery of small items that are (urgently) needed in locations with difficult access.

We have a fleet of **10 drones**. A drone is capable of carrying devices, other than cameras, and capable of delivering small loads. For our use case **the load is medications**.

## Features
- Registering a Drone
- Loading drone with medications items
- Checking loaded medication items for a given drone
- Checking available drones for loading
- Check drone battery level for a given drone

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
$ git clone https://github.com/josueisaihs/drones
```
Create virtual environment and activate it:
```sh
$ python3 -m venv env/
source env/bin/activate
```
Install dependencies:
```sh
$ cd src
$ pip install -r requirements.txt
```
Create the database file and create the models in the database:
```sh
$ cd drones
$ ./manage.py migrate
```
#### Load data to test the app
Create data tot test the app:
```sh
$ ./manage.py create_data --all
```
(optional) Added custom commands to add and remove data for testing the app.
The create command options are:
```sh
./manage.py create_data [--all] [--drone] [--medications] [--package]
optional arguments:
--drone         Create 10 drones with random data 
--medication    Create medications with random data
--package       Create packets with random data
--user          Create user, username: "admin" and password: "password"
--all           Create all the above data
```
The remove command options are:
```sh
./manage.py clean_data [--all] [--drone] [--medications] [--package] [--delivery]
optional arguments:
--drone         Remove drones
--medication    Remove medications
--package       Remove packets
--delivery      Remove delivery packages
--all           Remove all data
```
The battery charge command options are:
```sh
$ ./manage.py charge_batteries [--random]
optional arguments:
--random         Provides a random value between 10 and 100 for the battery status
```
Charge the drones that are in Low Battery and their state is other than IDLE, to a state of charge of 100%.
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
$ ./manage.py runserver
```
#### Redis
First download [Redis](https://download.redis.io/releases/redis-6.2.6.tar.gz) and read the ``README`` file.
Open the downloaded folder in the another terminal and simply run:
```sh
$ make
```
After building Redis, it is a good idea to test it using:
```sh
$ make test
```
To run Redis with the default configuration, just type:
```sh
$ cd src
$ ./redis-server
```
You can use redis-cli to play with Redis. Start a redis-server instance,
then in another terminal try the following:
```sh
$ cd src
$ ./redis-cli
$ redis> ping
PONG
$ redis>quit
```
#### Celery
Open a new instance of the terminal in the project's containing folder to initialize celery:
```sh
$ source env/bin/activate
$ cd src/drones
$ celery -A drones worker -l info
```
And open an another instance of the terminal in the project's containing folder and run the following:
```sh
$ source env/bin/activate
$ cd src/drones
$ celery -A drones beat -l info
```

### Test
---
To run the tests, try the following:
```sh
$ ./migrate test
```
### API
---
#### Drones
The serial number can only have up to 100 characters.
A drone can load up to ``MAX_WEIGHT``, configured in the ``settings.py``.
The states ``IDLE``, ``LOADING``, ``LOADED``, ``DELIVERING``, ``DELIVERED``, ``RETURNING``. A drone can only receive a charge if it is in ``IDLE`` state

To create, retrieve, update and destroy drones:

``Create and List``
[http://localhost:8000/drone-delivery/api/drone/list/](http://localhost:8000/drone-delivery/api/drone/list/)

``Retrieve, Update, Destroy``
[http://localhost:8000/drone-delivery/api/drone/slug/detail/](http://localhost:8000/drone-delivery/api/drone/list/)

JSON format that accepts to ``create``, ``retrieve``, ``update`` and ``destroy``:
```json
{
    "serial_number": <String>,
    "model": <String: Cruiserweight, Lightweight, "Middleweight, Cruiserweight, Heavyweight>,
    "weight_limit": <Float>,
    "battery_capacity": <Int>,
    "state": <String: IDLE, LOADING, LOADED, DELIVERING, DELIVERED, RETURNING>
}
```

JSON format to ``list`` results:
```json
{
    "id": <Int>,
    "slug": <String>,
    "serial_number": <String>,
    "model": <String: Cruiserweight, Lightweight, "Middleweight, Cruiserweight, Heavyweight>,
    "weight_limit": <Float>,
    "battery_capacity": <Int>,
    "state": <String: IDLE, LOADING, LOADED, DELIVERING, DELIVERED, RETURNING>
}
```
#### Medications
The name field Allow only letters [A-Za-z], numbers [0-9], "-" and underscore 
The code field allow only upper case letters [A-Z], underscore and numbers [0-9]
A medication can have a maximum weight of ``MAX_WEIGHT``, configured in the ``settings.py``.

To create, retrieve, update and destroy medications:

``Create and List``
[http://localhost:8000/drone-delivery/api/medication/list/](http://localhost:8000/drone-delivery/api/medication/list/)

``Retrieve, Update, Destroy``
[http://localhost:8000/drone-delivery/api/medication/slug/detail/](http://localhost:8000/drone-delivery/api/medication/list/)

JSON format that accepts to ``create``, ``retrieve``, ``update`` and ``destroy``:
```json
{
    "name": <String>,
    "weight": <Float>,
    "code": <String>,
    "image": <Image>
}
```

JSON format to ``list`` results:
```json
{
    "id": <Int>,
    "slug": <Slug>,
    "name": <String>,
    "weight": <Float>,
    "code": <String>,
    "image": <URL>
}
```
#### Packages
A package is a certain medication with the respective quantity.
A package can have a maximum weight of ``MAX_WEIGHT``, configured in the ``settings.py``.

To create, retrieve, update and destroy medications:

``Create and List``
[http://localhost:8000/drone-delivery/api/package/list/](http://localhost:8000/drone-delivery/api/package/list/)

``Retrieve, Update, Destroy``
[http://localhost:8000/drone-delivery/api/package/slug/detail/](http://localhost:8000/drone-delivery/api/package/list/)

JSON format that accepts to ``create``, ``retrieve``, ``update`` and ``destroy``:
```json
{
    "medication": <Medication.pk>,
    "qty": <Int>
}
```

JSON format to ``list`` results:
```json
{
    "id": <Int>,
    "slug": <Slug>,
    "medication": {
        "name": <String>,
        "slug": <Slug>
    },
    "qty": <Int>,
    "created": "%y-%m-%d %H:%M",
    "weight": <Float>
}
```
#### Deliveries Packages
A delivery package is to assign a drone a certain number of packages, as long as the drone is capable of supporting the weight of the load.
A drone is only available for loading when its battery is greater than ``LOW_BATTERY``, configured in the settings, and it is in ``IDLE`` state.

To create, retrieve, update and destroy deliveries packages:

``Create and List``
[http://localhost:8000/drone-delivery/api/delivery/list/](http://localhost:8000/drone-delivery/api/delivery/list/)

``Retrieve, Update, Destroy``
[http://localhost:8000/drone-delivery/api/delivery/slug/detail/](http://localhost:8000/drone-delivery/api/delivery/list/)

JSON format that accepts to ``create``, ``retrieve``, ``update`` and ``destroy``:
```json
{
    "drone": <Drone.pk>,
    "package": [<Package.pk>, <Package.pk>, ..., <Package.pk>]
}
```

JSON format to ``list`` results:
```json
{
    "slug": <Slug>,
    "drone": {
        "slug": <Slug>, 
        "serial_number": <String>, 
        "weight_limit": <Float>, 
        "battery_capacity": <Int>
    },
    "package": {
        "items": [
            {
                "id": <Int>,
                "slug": <Slug>, 
                "weight": <Float>, 
                "qty": <Int>,
                "medication": {
                    "slug": <Slug>,
                    "name": <String>
                }
            }
        ],
        "weight": <Float>
    }
}
```

## Examples
---
Below is the sequence to create a delivery order.
```sh
$ curl -X GET http://127.0.0.1:8000/drone-delivery/api/drone/list/
```
Using the ``admin`` and ``password`` credentials a drone is registered:
```sh
$ curl -u 'admin:password' -d '{"serial_number": "456345647", "model": "Cruiserweight", "weight_limit": 400.0, "battery_capacity": 98, "state": "IDLE"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/drone-delivery/api/drone/list/
```
Now the package should be created:
```sh
$ curl -u 'admin:password' -d '{"medication": 1, "qty": 1}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/drone-delivery/api/package/list/
{"id":14,"slug":"acetaminophen-1","medication":{"name":"Acetaminophen","slug":"acetaminophen-x5pjf530s0"},"qty":1,"created":"2022-01-17 00:37","weight":3.0}%  
$ curl -u 'admin:password' -d '{"medication": 2, "qty": 1}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/drone-delivery/api/package/list/
{"id":15,"slug":"adenosine-1","medication":{"name":"Adenosine","slug":"adenosine-uxv"},"qty":1,"created":"2022-01-17 00:41","weight":7.0}%
```
Finally, the drone is assigned (id = 14) and the packages created (id = 14, id = 15) to form the delivery package:
```sh
$ curl -u 'admin:password' -d '{"drone": 14, "package": [14, 15]}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/drone-delivery/api/delivery/list/
{"slug":"456345647","drone":{"slug":"456345647","serial_number":456345647.0,"weight_limit":400.0,"battery_capacity":74},"package":{"items":[{"slug":"acetaminophen-1","weight":3.0,"qty":1,"medication":{"slug":"acetaminophen-x5pjf530s0","name":"Acetaminophen"}},{"slug":"adenosine-1","weight":7.0,"qty":1,"medication":{"slug":"adenosine-uxv","name":"Adenosine"}}],"weight":10.0}}
```
## Admin
---
Django's [admin](localhost:8000/admin) view is also available. Use the ``admin`` and ``password`` credentials to authenticate.