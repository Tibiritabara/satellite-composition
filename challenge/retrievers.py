"""
This module will declare the helpers that will allow us to
retrieve the GeoTiff images even remotely or local
"""
import asyncio
import os
import fnmatch
import logging
import abc
import urllib.request
from random import randint
from time import sleep
from typing import Tuple
from urllib.error import HTTPError
from django.conf import settings
from challenge.exceptions import ChannelNotFound


logger = logging.getLogger(__name__)


class RetrieverInterface(abc.ABC):
    """
    Interface shared by the classes in charge of retrieving the
    base band data. This will allow us to include new retrievers
    from different sources.
    """

    @abc.abstractmethod
    def retrieve(self, name: str) -> str:
        """
        This method should retrieve the band file and return its
        path
        :param str name:
        :return:
        """
        pass


class CloudStorageRetriever(RetrieverInterface):
    """
    This class is in charge of retrieving the data directly from the google
    cloud storage. Its implementation is a little bit primitive as the only
    thing that does is an HTTP Request to google cloud storage. This is due
    to the fact that I dont have credentials to access it completely, and
    the library behind requires the use of it. If the access was given, this
    could explore the remote filesystem in an effective way.
    """
    def __init__(self, local: str, remote: str):
        self.local = local
        self.remote = remote

    def retrieve(self, name: str) -> str:
        """
        Retrieve a file from the remote storage
        :param name:
        :return:
        """
        try:
            location, _ = urllib.request.URLopener().retrieve(
                "%s%s" % (self.remote, name),
                "%s%s" % (self.local, name),
            )
            return location
        except HTTPError:
            raise ChannelNotFound()


class LocalStorageRetriever(RetrieverInterface):
    """
    This class is in charge of retrieving the band data stored or cached
    in the local filesystem.
    """
    def __init__(self, local: str):
        self.local = local

    def retrieve(self, name: str) -> str:
        """
        Looks for the file on the configured cache folder. This configuration
        can be retrieved from the settings file
        :param str name:
        :return str:
        """
        files = os.listdir(self.local)
        for file in files:
            if fnmatch.fnmatch(file, name):
                return "%s%s" % (
                    self.local,
                    file
                )
        raise ChannelNotFound()


class Retriever:
    """
    Main retriever, it works as an oversimplified strategy pattern.
    It orchestrates the retrievers in order to allow the user to
    explore both filesystems.
    """
    async def retrieve(self, name: str, channel: str) -> Tuple[str, str]:
        """
        This method allows us to explore both filesystems for a given band
        :param str name:
        :param str channel:
        :return:
        """
        try:
            return LocalStorageRetriever(self.__get_local_cache()).retrieve(
                "%s*%s.tif" % (
                    name,
                    channel,
                )
            ), channel
        except ChannelNotFound:
            if not self.__get_remote_url():
                raise ChannelNotFound()

            return CloudStorageRetriever(
                self.__get_local_cache(),
                self.__get_remote_url(),
            ).retrieve(
                "%s%s.tif" % (
                    name,
                    channel,
                )
            ), channel

    def retrieve_generated(self, name: str, channel_map: str):
        """
        This method allows us to retrieve an already generated image that was cached.
        As this process is expensive, is better to cache the response images to
        retrieve them at a later point
        :param str name:
        :param str channel_map:
        :return:
        """
        try:
            return LocalStorageRetriever(self.__get_generation_cache()).retrieve(
                "%s%s.jpg" % (
                    name,
                    channel_map,
                )
            )
        except ChannelNotFound:
            logger.info("There is no cached file for:", name, channel_map)
            return False

    def __get_local_cache(self) -> str:
        """
        Retrieve the local storage setting
        :return:
        """
        return getattr(settings, 'GEOTIFF_STORAGE', {})['LOCAL_STORAGE']

    def __get_remote_url(self) -> str:
        """
        Retrueve the remote storage setting
        :return:
        """
        return getattr(settings, 'GEOTIFF_STORAGE', {})['REMOTE_STORAGE']

    def __get_generation_cache(self) -> str:
        """
        Retrieve the generated images storage
        :return:
        """
        return getattr(settings, 'GEOTIFF_STORAGE', {})['GENERATION_STORAGE']
