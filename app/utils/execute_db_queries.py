"""
Centralized script to execute database queries
"""
from settings import settings
import logging
import json
import uuid

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

def execute(query: str):
    try:
        con = settings.get_mariadb_cursor()
        cur = con.cursor()

        cur.execute(query)
        con.commit()
        with open("../storage/db_out.txt", "w") as file:
            for i in cur:
                file.write(str(i))
        
    except Exception as e:
        print(f"Exception Occurred while running mariadb query - {query} as {e}")
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'con' in locals() and con:
            con.close()

def insert_data():

    with open("../storage/movie_listings.json", "r") as file:
        data = json.load(file)

    for dict_list in data:
        movie_uuid = None
        
        # Logic to read video files of a movie
        if len(dict_list["video_files"]) > 0:
            for movie_file in dict_list["video_files"]:
                movie_uuid = uuid.uuid4()
                query = f"""INSERT INTO movies(name, movie_uuid, creation_date, last_update_date, file_location) 
                            values ('{movie_file.replace("'", "")}', '{movie_uuid}', CURDATE(), CURDATE(), '{dict_list['path'].replace("'", "")}')"""
                execute(query)

        # Logic to read all the other files of a movie    
        if len(dict_list["other_files"]) > 0:
            for other_file in dict_list["other_files"]:
                query = f"""INSERT INTO movie_attributes(movie_id, movie_uuid, attribute_name, attribute_value, creation_date, 
                            last_update_date, attribute1, attribute2, attribute3, attribute4, attribute5)
                            values(NULL,'{movie_uuid}', 'OTHER FILES', '{other_file.replace("'", "")}', CURDATE(), 
                            CURDATE(),NULL, NULL, NULL, NULL, NULL)"""
                execute(query)

        # Logic to read all the subtitle files of a movie    
        if len(dict_list["subtitles"]) > 0:
            for other_file in dict_list["subtitles"]:
                query = f"""INSERT INTO movie_attributes(movie_id, movie_uuid, attribute_name, attribute_value, creation_date, 
                            last_update_date, attribute1, attribute2, attribute3, attribute4, attribute5)
                            values(NULL,'{movie_uuid}', 'SUBTITLES', '{other_file.replace("'", "")}', CURDATE(), 
                            CURDATE(),NULL, NULL, NULL, NULL, NULL)"""
                execute(query)

if __name__ == "__main__":
    execute("select * from movies")