from app.utils.settings import settings
from app.crawlers.get_objects import generate_db_movie_document
from app.utils.schema import mongodb_object_operation_return, movie_uuid, mongo_refresh, \
                             GetMoviePagesRequest, GetMoviePages, MovieObject
from fastapi import APIRouter

import logging

logger = logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

router = APIRouter()

"""
This method is to update documents in MongoDB
There are 2 input parameters:
    1) location - This is the location to scan for media
    2) mode - This tells the app whether to delete the documents or append
"""
@router.post("/refresh", response_model=mongodb_object_operation_return, summary="Update Mongodocs")
async def scan_and_insert_mongo_objects(request: mongo_refresh) \
    -> mongodb_object_operation_return:
    
    ret_resp = mongodb_object_operation_return(location=request.location)
    ret_resp.mode = request.mode

    # Get the database object
    dbname = settings.get_database()
    
    if dbname is not None:
        # You can now use the dbname object to interact with collections and data
        logger.debug(f"Database object: {dbname}")
        collection = dbname['movies']
        
        if request.mode == "refresh":
            del_result = collection.delete_many({})
            ret_resp.deleted_count = del_result.deleted_count
            
        collection.insert_many(generate_db_movie_document(location=request.location))
        
        # result = collection.find({"_id" : f"{ret_resp.insert_ids[0]}"})
        result = collection.find()
        for doc in result:
            insert_dict = movie_uuid()
            insert_dict.uuid = doc["_id"]
            insert_dict.name = doc["name"]
            ret_resp.insert_ids.append(insert_dict.get_dict())
        
    return ret_resp.get_dict()

"""
This method is to get documents from MongoDB using pagination
There are 3 input parameters:
    1) offset - This is the location to scan for media
    2) limit - This tells the app whether to delete the documents or append
    3) 
"""
@router.post("/movies", response_model=GetMoviePages, summary="Get Mongodocs")
async def get_mongo_docs(request: GetMoviePagesRequest) \
    -> GetMoviePages:

    logger.debug(f"Request Limit = {request.limit}")
    logger.debug(f"Request Offset = {request.offset}")
    logger.debug(f"Request Query = {request.query}")

    ret_resp = GetMoviePages()
    iter = 0
    
    logger.debug("Instantiating DB object")
    # Get the database object
    dbname = settings.get_database()
    
    if dbname is not None:
        # You can now use the dbname object to interact with collections and data
        logger.debug(f"Database object: {dbname}")
        collection = dbname['movies']

        result = collection.find(request.query).sort({"_id": 1}).skip(request.offset).limit(request.limit)

        ret_resp.total_records = collection.count_documents(request.query)
        ret_resp.limit = request.limit
        ret_resp.offset = request.offset
        for doc in result:
            ret_resp.movie_docs.append(doc)
            ret_resp.movie_docs[iter]["id"] = doc["_id"]
            iter+= 1

    return ret_resp.get_dict()

"""

"""
@router.put("/movies", summary="Update Mongodocs")
async def update_mongo_doc(request: MovieObject):
    ret_resp = MovieObject()

    filter = {"_id" : request.id}
    
    # Get the database object
    dbname = settings.get_database()
    collection = dbname['movies']

    result = collection.find_one(filter)

    logger.debug(result)
    req_dict = request.__dict__
    
    print(request.id)
    ret_resp.id = request.id
    extract_key = (lambda result, key, req_dict: result[key] if req_dict[key] is None else req_dict[key])
    ret_resp.name = extract_key(result=result, key="name", req_dict=req_dict)
    ret_resp.year = extract_key(result=result, key="year", req_dict=req_dict)
    ret_resp.language = extract_key(result=result, key="language", req_dict=req_dict)
    ret_resp.movie_file = extract_key(result=result, key="movie_file", req_dict=req_dict)
    if len(result["cast_crew"]) > 0:
       ret_resp.cast_crew = request.cast_crew.append(result["cast_crew"])
    if len(result["genre"]) > 0:
        ret_resp.genre = request.genre.append(result["genre"])
    if len(result["tags"]) > 0:
        ret_resp.tags = request.tags.append(result["tags"])
    if len(result["photos"]) > 0:
        ret_resp.photos = request.photos.append(result["photos"])
    if len(result["additional_video_files"]) > 0:
        ret_resp.additional_video_files = request.additional_video_files.append(result["additional_video_files"])
    if len(result["subtitles"]) > 0:
        ret_resp.subtitles = request.subtitles.append(result["subtitles"])

    collection.update_one(filter, {"$set" : ret_resp.get_dict()}, upsert=False)

    return ret_resp.get_dict()