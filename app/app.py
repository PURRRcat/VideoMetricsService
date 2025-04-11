from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from gstreamer import encode_and_decode
from postgresql import PostgresAPI
from typing import List

app = FastAPI()

class VideoData(BaseModel):
    video_path: str
    codec: str

class VideoDataMerge(BaseModel):
    video_path: List[str]
    codec: str


# @app.get("/")
# def read_root():
#     return {}


@app.post("/merge")
def post_item(video_data: VideoDataMerge, background_tasks: BackgroundTasks):
    with PostgresAPI() as db:
        task_id, status = db.insert()
    background_tasks.add_task(encode_and_decode, video_id=task_id, input_path=video_data.video_path, codec=video_data.codec)
    return {"video_id": task_id, "status": status}

@app.post("/video")
def post_item(video_data: VideoData, background_tasks: BackgroundTasks):
    with PostgresAPI() as db:
        task_id, status = db.insert()
    background_tasks.add_task(encode_and_decode, video_id=task_id, input_path=[video_data.video_path], codec=video_data.codec)
    return {"video_id": task_id, "status": status}


@app.get("/video/status/{video_id}")
def get_status(video_id: int):
    with PostgresAPI() as db:
        status = db.get_status(video_id)
    return {"status": status}

@app.get("/video/{video_id}")
def read_item(video_id: int):
    with PostgresAPI() as db:
        if db.get_status(video_id) == 'done':
            video_size, encoding_time, decoding_time = db.get_id(video_id)
            return {f"video_size: {video_size:.2f} MB, encoding_time: {encoding_time:.2f} sec, decoding_time: {decoding_time:.2f} sec"}
        else:
            return {"status": db.get_status(video_id)}

@app.delete("/video/{video_id}")
def read_item(video_id: int):
    with PostgresAPI() as db:
        db.delete_video(video_id)
    return {"video_id": video_id}