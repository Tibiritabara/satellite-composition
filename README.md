# Interstellar
## Backend tech challenge

### Description
The goal was to create a microservice able to handle a single endpoint. This endpoint requires
a json in the next way:

```json
{
  "utmZone": "33",
  "latitudeBand": "U",
  "gridSquare": "UP",
  "date": "2014-05-05",
  "channelMap": "visible"
}
```
The data sent will be validated and based on that information we are able to retrieve satellite data
in compliance with sentinel-2 bands. Based on these retrieved GeoTiff we are finally able
to build a jpeg image according to the channelMap specified on the user request.
There are 3 available channelMaps: visible, vegetation and waterVapor.

### Tech stack
The project was created with the help of Django and Djangorestframework. It is running using 
pipenv for dependency and environment management, and finally it can be tested with the help
of docker.

### Components
The project has the next elements:
* Support for .env giving us flexibility when deploying to different environments.
* Djangorestframework provided the use of serializers for input validation and views
for easy data handling. The framework might be an overkill, and Flask could have been
a better alternative for this single operation, but django gives a boost in stability and
allow us to keep building on top without too much hassle.
* There is OpenAPI Swagger documentation available on the route /docs.
* The main modules of the tool are:
    * Retriever: which is a collection of classes sharing the same interface in order to 
    retrieve the GeoTiff images from different sources. There are limitations due to the
    restricted access to the cloud storage (there are no credentials that can be configured).
    The operation is the next one: the project will look for the resources locally, these might 
    be stored on the *cache* folder that is visible on the root of the project. If the files do
    not exist in that folder it will try to retrieve them vis HTTP request from google cloud
    storage urls. The issue with cloud storage is that then a datetime object must be handled
    in order to be available to use it correctly. The best solution is to use google credentials
    to access the bucket and use it as a virtual filesystem, but at the moment is impossible with
    only the public access.
    This can be configured on the django settings like this:
    ```
    GEOTIFF_STORAGE = {
        "LOCAL_STORAGE": os.getenv('LOCAL_STORAGE'),
        "REMOTE_STORAGE": os.getenv('REMOTE_STORAGE'),
        "GENERATION_STORAGE": os.getenv('GENERATION_STORAGE'),
    }
    ```
    Or just by modifying the .env file with the new folders and remote urls.
    * Builder: This module puts everything together. It takes the name of the file and it retrieves
    the required bands by using the retriever classes. The bands are setted by a configuration entry
    on the settings.py file from django. In order to grow the number of available channelMaps, it is just 
    enough with building a new mapper on the django settings and then extending the serializer validations
    . This is how the settings look like:
    ```
    GEOTIFF_MAPPERS = {
        "visible": {
            "B02": "B",
            "B03": "G",
            "B04": "R",
        },
        "vegetation": {
            "B05": "R",
            "B06": "G",
            "B07": "B",
        },
        "waterVapor": {
            "B09": "B",
        },
    }
    
    ```
    Where RGB are the Red, Green and Blue color channels, which are mapped to a given band. When the 
    final image is generated from the mapping, it will be stored on the cache/generated folder
    in order to avoid rerunning the operation when receiving the same request in a future opportunity.
    To process the GeoTiff images I made use of rasterio available on https://rasterio.readthedocs.io/en/latest/.
    This tool is based on Gdal for ubuntu.


### How to run it
Fortunately docker is here to save the day. We can just:
```
docker build -t interestellar .
```

and then
```
docker run -p 8080:8080 interestellar
```

In order to see the swagger documentation please go to http://localhost:8080/docs

To trigger the endpoint just POST http//localhost:8080/generate-image with the specified json body

If you want to run it locally with all the python deps, just ensure that you have python 3.7 installed
and follow the next steps:

* Install Pipenv if you don't have it already ([download here](https://pipenv.readthedocs.io/en/latest/)): $`pip install --user pipenv`
* then run `pipenv install` on the project folder. This will create a virtual environment with all 
of the dependencies inside.
* Execute `cp .env.dist .env` to ensure the environment variables are loaded.
* To run the server you can use django builtin servier with `pipenv run python manage.py runserver`
This will run the project on the port 8000. The use of pipenv is important, as this package 
manager is the one loading the .env files
* Place the granules on the `cache` folder of the project.

And finally to run the tests pls:
* Run `PIPENV_DOTENV_LOCATION=.env.test pipenv run python manage.py test` in order to override
the .env file and use the testing configuration.
* If for some reason the tests fail due to the `tkinter` module missing, please do 
`sudo apt install python-tk`

The code is completely documented, and the tests have a 90+% of coverage. There is room for improvement
everywhere, and the logs could be better, but it was an amazing experience to work on it.

