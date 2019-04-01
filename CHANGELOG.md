# Changelog


## 1.0.0

- Refactor(geotiff): use executor to loop through the file processing.
  [Ricardo Santos Diaz]

  After yesterday changes there were doubts on how rasterio dealed with the files. Hose are executed in a blocking way due to the fact that it access the filesystem. The best way to fight that is to use executors. The change shows a 30% improvement on loading times
- Fix(project): remove a bug when calling run method on async. [Ricardo
  Santos Diaz]
- Docs(project): Add async description on readme. [Ricardo Santos Diaz]
- Feat(geotiff): add async support for retrieving and mapping channels.
  [Ricardo Santos Diaz]

  In order to improve performance, the project now uses the async method definitions from python in order to run the tasks in parallel.
- Build(project): remove .idea folder. [Ricardo Santos Diaz]
- Ci(project): The image is not pushed to the docker registry. [Ricardo
  Santos Diaz]
- Ci(project): Fix to build stage on gitlab_ci. [Ricardo Santos Diaz]
- Test(project): change the test image source dependency. [Ricardo
  Santos Diaz]
- Ci(project): rolled back pipenv changes on test script. [Ricardo
  Santos Diaz]
- Ci(project): tests are failing on the ci env due to .env vars.
  [Ricardo Santos Diaz]
- Test(project): Changed the test to waterVapor to reduce memory usage
  on CI. [Ricardo Santos Diaz]
- Ci(project): Fix to CI pipeline failing due to missing python deps.
  [Ricardo Santos Diaz]
- Ci(project): Add gitlab_ci to support test and build stages. [Ricardo
  Santos Diaz]
- Docs(project): add the readme file with the project description.
  [Ricardo Santos Diaz]
- Test(project): Add functional tests with more than 90% coverage.
  [Ricardo Santos Diaz]

  We needed tests, by personal experience, the best way to test is through the use of functional testing. The tests could be bigger and more complete, but a good coverage was managed.
- Feat(geotiff): Get band images and build result based on map settings.
  [Ricardo Santos Diaz]

  There is a lot to unpack. There is now support for env variables that are bing used in the settings file. Lots of the functionality was created on a dynamic way which gives us flexibility. The channel maps can also be defined dynamically on the settings.
- Feat(geotiff): create filename and configure channel_map on settings.
  [Ricardo Santos Diaz]

  There is now the option to dinamically create channel_maps by using the django settings configuration. Also, when looking for a file on the local_storage now we look for regular expressions, in order to avoid requiring time. As the remote_storage is more expensive, due to the fact that we are hitting the url, and is hard to define the time as a regular expression, it is not supported.
- Feat(geotiff): Retrieve from local or remote storage the GeoTiff file.
  [Ricardo Santos Diaz]

  The plan is to make the tool as flexible as possible. It will try to retrieve the geotiff files from local storage according to environment variables and project settings. If the file does not exist it falls back to a remote url and it tries to get the files directly from the google cloud storage, and after that stores it in the local cache in order to reduce the effort on a subsequent request
- Feat(challenge): add serialization, views, docs and validation.
  [Ricardo Santos Diaz]
- Build(project): add the dockerfile. [Ricardo Santos Diaz]
- Build(project): create the project and add the base dependencies.
  [Ricardo Santos Diaz]


