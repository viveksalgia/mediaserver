"""
Docstring for app.crawlers.get_objects
Centralized place to get the objects from SFTP
and convert them into MongoDB documents
"""
import json
import logging
import uuid
import base64

# Relative imports
from app.utils.settings import settings
from app.utils.execute_shell import execute_cmd
from app.utils.schema import MovieObject, Subtitles, AdditionalVideoFiles, Photos

logger = logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

"""
Method to call execute_cmd by passing the command and
generating a response file as MongoDB Movie document
"""
def generate_db_movie_document(location: str) -> list[MovieObject]:

    file_arr: list[MovieObject] = []

    # List the location
    cmd = ["ls", location]
    logger.debug(f"Command to be executed - {' '.join(cmd)}")

    response = execute_cmd(cmd=cmd)
    logger.debug(f"Command Response - {'\n'.join(response['std_out'])}")

    """ 
        Loop through the response files
        Assumption:
            Folder structure of the movie listing is one level only.
            Bollywood/<Folder(MovieName)>/All the files 
    """
    for folder in response['std_out']:

        logger.debug("Instantiating a movie object")
        movie_object = MovieObject()
        movie_object.id = str(uuid.uuid4())
        movie_object.name = folder
        cmd = ["ls", f"{location}/{folder}"]
        logger.debug(f"Command to be executed - {' '.join(cmd)}")

        response_sub = execute_cmd(cmd=cmd)
        logger.debug(f"Command Response - {'\n'.join(response_sub['std_out'])}")

        for file in response_sub['std_out']:
            logger.debug(f"Folder name - {folder} and File is {file}")
            if (file.find(".mp4") > -1 or file.find(".mkv") > -1 or file.find(".avi") > -1) and file.find(folder) > -1:
                movie_object.movie_file = f"{location}/{folder}/{file}"
            elif file.find(".srt") > -1 or file.find(".sub") > -1:
                subtitles = Subtitles()
                subtitles.file = f"{location}/{folder}/{file}"
                movie_object.subtitles.append(subtitles.get_dict())
            elif (file.find(".mp4") > -1 or file.find(".mkv") > -1 or file.find(".avi") > -1):
                additional_video_files = AdditionalVideoFiles()
                additional_video_files.file = f"{location}/{folder}/{file}"
                additional_video_files.type = "Sample"
                movie_object.additional_video_files.append(additional_video_files.get_dict())
            elif (file.find(".jpg") > -1 or file.find(".png") > -1 or file.find(".jpeg") > -1):
                photos = Photos()
                photos.filename = file
                with open(f"{location}/{folder}/{file}", "rb") as file:
                    photos.imageb64 = base64.b64encode(file.read()).decode('utf-8')
                    photos.thumbnail = "Y"
                movie_object.photos.append(photos.get_dict())

        file_arr.append(movie_object.get_dict())

    return file_arr



