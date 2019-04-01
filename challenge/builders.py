"""
This module contains all the classes and methods related with the
jpeg creation
"""
import asyncio
import logging
import rasterio as rio
import numpy as np
from concurrent import futures
from django.conf import settings
import matplotlib.pyplot as plt
from challenge.retrievers import Retriever


logger = logging.getLogger(__name__)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


class Builder:
    """
    This interface defines the base behavior shared by all
    builders, based on the channel_map
    """
    EXTENSION = "jpg"

    def __init__(self, channel_map: str):
        self.channel_map = channel_map
        self.mapping = self.__get_mapping(channel_map)

    def build(self, name: str) -> str:
        """
        This method orchestrates the operations between image retrieval
        and image construction using rasterio, numpy and matplotlib
        :param str name: name of the files
        :return str: path of the generated file
        """
        # Try to retrieve the file from the cache
        cached = Retriever().retrieve_generated(
            name,
            self.channel_map,
        )
        if cached:
            return cached

        # If there ios no cache, build a new image
        files = self.get_channels(name)
        files = self.map_channels(files)
        path = "%s%s%s.%s" % (
            self.__get_generation_cache(),
            name,
            self.channel_map,
            self.EXTENSION,
        )

        # As we can have one or more channels we take the first
        # one as a guide to know the dimensions of the image
        tempkey = None
        for key in files.keys():
            tempkey = key
            break

        plt.imsave(
            path,
            np.dstack((
                files.get("R", np.zeros_like(files.get(tempkey))),
                files.get("G", np.zeros_like(files.get(tempkey))),
                files.get("B", np.zeros_like(files.get(tempkey))),
            ))
        )
        return path

    def get_channels(self, name) -> dict:
        """
        Retrieve the images by band
        :param str name:
        :return dict:
        """
        tasks = []
        files = dict()
        for channel in self.mapping.keys():
            tasks.append(loop.create_task(
                Retriever().retrieve(
                    name,
                    channel,
                )
            ))

        responses = loop.run_until_complete(asyncio.gather(*tasks))
        for response, channel in responses:
            files[self.mapping[channel]] = response
        return files

    def map_channels(self, files: dict) -> dict:
        """
        Map the bands to the RGB channels
        :param dict files:
        :return:
        """
        tasks = []
        executor = futures.ThreadPoolExecutor(max_workers=5)
        for key, value in files.items():
            tasks.append(loop.run_in_executor(
                executor,
                self.__normalize,
                key,
                value,
            ))
        responses = loop.run_until_complete(asyncio.gather(*tasks))
        for response, channel in responses:
            files[channel] = response
        return files

    def __normalize(self, channel: str, file: str):
        """
        Normalizes numpy arrays into scale 0.0 - 1.0
        :param array:
        :return
        """
        array = rio.open(file).read(1)
        array_min, array_max = array.min(), array.max()
        mean = ((array - array_min) / (array_max - array_min))
        logger.info(
            "Normalized bands:",
            array_min,
            "-",
            array_max,
            "mean:",
            mean,
        )
        return mean, channel

    def __get_mapping(self, channel_map: str) -> dict:
        """
        Get the mapping settings
        :param channel_map:
        :return:
        """
        return getattr(settings, 'GEOTIFF_MAPPERS', {})[channel_map]

    def __get_generation_cache(self) -> str:
        """
        Get the final cache location
        :return:
        """
        return getattr(settings, 'GEOTIFF_STORAGE', {})['GENERATION_STORAGE']
