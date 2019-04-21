# BLUEbikes Dashboard Project

A project to provide REST APIs of BLUEBikes data (Stations and Trips) and dashboard to visualize their summary

## Data

The data can be downloaded from the [BLUEbikes site](https://www.bluebikes.com/system-data). Especially, the following data are used in this project:

* Region information: https://gbfs.bluebikes.com/gbfs/en/system_regions.json
* Station information: https://gbfs.bluebikes.com/gbfs/en/station_information.json
* Trip information: https://s3.amazonaws.com/hubway-data/index.html (You can choose any monthly dataset named as 'YYYYmm-bluebikes-tripdata.zip')

which are also referred at [HealthData.gov](https://healthdata.gov/dataset/hubway-system-data).

## Getting Started

### Prerequisites

What things you need to install the software and how to install them

```
Python 2.7.15
pip 19.0.3
```

### Installing

1. Load required libraries

```
pip install -r requirements.txt
```

2. Create database and import some master data (Note: you need to connect to internet because this automatically gets the datasets mentioned above.)

```
python manage.py migrate
```

3. Start the server

```
python manage.py runserver
```

4. 

## Running the tests

```
python manage.py test
```

## Built With

* [Django](https://www.djangoproject.com/) - The high-level Python Web framework
* [Django REST framework](https://www.django-rest-framework.org/) - The toolkit for building Web APIs
* [django-filter](https://django-filter.readthedocs.io) - The toolkit to alleviate writing some of the more mundane bits of view code

