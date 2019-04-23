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

2. Download one Bluebikes trip history data from [here](https://s3.amazonaws.com/hubway-data/index.html), unzip the file and put a csv file into the data folder.

3. Create database and import some master data (Note: you need to connect to internet because this automatically gets the Region and Station datasets mentioned above). It will take for a while depending on how large your dataset is. 

```
python manage.py migrate
```

4. Start the server

```
python manage.py runserver
```

If you can see the Api Root page at http://127.0.0.1:8000/apis via any browser, you have completed installation!

You can also access to the dashboard via http://127.0.0.1:8000/dashboards/.

### API docs

You can see the list of all the endpoints and their specifications at http://127.0.0.1:8000/docs/.

You can also see the explanations of each endpoint at http://127.0.0.1:8000/apis.

## Running the tests

```
python manage.py test
```

## Built With

* [Django](https://www.djangoproject.com/) - The high-level Python Web framework
* [Django REST framework](https://www.django-rest-framework.org/) - The toolkit for building Web APIs
* [django-filter](https://django-filter.readthedocs.io) - The toolkit to alleviate writing some of the more mundane bits of view code
* [drf-dynamic-fields](https://github.com/dbrgn/drf-dynamic-fields) - a mixin to dynamically limit the fields per serializer to a subset specified by an URL parameter

* [jQuery](https://jquery.com/) - The JavaScript library to make client development much simpler with an easy-to-use API
* [d3.js](https://d3js.org/) - The JavaScript library for manipulating documents based on data
* [Bootstrap](https://getbootstrap.com/) - The front-end component library: the design of this dashboard is based on its [example](https://getbootstrap.com/docs/4.3/examples/dashboard/).
* [Font Awesome](https://fontawesome.com/) - The icon set and toolkit

