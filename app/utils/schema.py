from pydantic import BaseModel, Field
from typing import List

class shell_cmd_output(BaseModel):
    cmd: List[str] = Field(..., description="List of Commands to be executed as part shell")
    std_out: List[str] = Field(default=None, description="Output of the command as captured by standard out")
    std_err: List[str] = Field(default=None, description="Error if any from the command execution as captured by standard err")

    def __init__(self, cmd, std_out, std_err):
        super().__init__(cmd=cmd, std_out=std_out, std_err=std_err)
        self.cmd = cmd
        self.std_out = std_out
        self.std_err = std_err
        

    def get_dict(self):
        return {"cmd" : self.cmd, "std_out" : self.std_out, "std_err" : self.std_err}

class CastCrew(BaseModel):
    name: str = Field(default=None, description="Name of the cast or crew member")
    profile: str = Field(default=None, description="Link to the profile if any")
    character_name: str = Field(default=None, description="Name of the character played by the cast if any")

    def get_dict(self):
        return {
                "name": self.name,
                "profile": self.profile,
                "character_name": self.character_name
                }
    
class Photos(BaseModel):
    imageb64: str = Field(default=None, description="Base64 encoded string to store the photo file")
    thumbnail: str = Field(default=None, description="Thumbnail file flag")
    primary: str = Field(default=None, description="Primary file flag")
    filename: str = Field(default=None, description="Name of the photo/poster file")

    def get_dict(self):
        return {
                "imageb64": self.imageb64,
                "thumbnail": self.thumbnail,
                "primary": self.primary,
                "filename" : self.filename
                }

class AdditionalVideoFiles(BaseModel):
    file: str = Field(default=None, description="Additional video filename")
    type: str = Field(default=None, description="Type of additional video file")

    def get_dict(self):
        return {
                "file": self.file,
                "type": self.type
                }

class Subtitles(BaseModel):
    file: str = Field(default=None, description="Subtitle file name")
    language: str = Field(default=None, description="Language of the subtitles")

    def get_dict(self):
        return {
                "file": self.file,
                "language": self.language
                }

class MovieObject(BaseModel):
    id: str = Field(default=None, description="Movie UUID used to uniquely identify the movie")
    name: str = Field(default=None, description="Name of the movie")
    year: int = Field(default=None, description="Movie year when the movie was released")
    language: str = Field(default=None, description="Movie Language")
    cast_crew: list[CastCrew] = Field(default=[], description="List of Cast and Crew of the movie")
    genre: list[str] = Field(default=[], description="List of movie genres")
    tags: list[str] = Field(default=[], description="List containing movie tags")
    movie_file: str = Field(default=None, description="Absolute path of the movie file")
    photos: list[Photos] = Field(default=[], description="List of movie thumbnails and posters")
    additional_video_files: list[AdditionalVideoFiles] = Field(default=[], description="List of any additional video files like samples")
    subtitles: list[Subtitles] = Field(default=[], description="List of movie subtitle files")

    def get_dict(self):
        return {
                "_id": self.id,
                "name": self.name,
                "year": self.year,
                "language": self.language,
                "cast_crew": self.cast_crew,
                "genre": self.genre,
                "tags": self.tags,
                "movie_file": self.movie_file,
                "photos": self.photos,
                "additional_video_files": self.additional_video_files,
                "subtitles": self.subtitles
                }
