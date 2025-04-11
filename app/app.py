from fastapi import FastAPI
from pydantic import BaseModel
from gstreamer import encode_and_decode
from postgresql import PostgresAPI

app = FastAPI()

class VideoData(BaseModel):
    video_path: str
    codec: str

# @app.get("/")
# def read_root():
#     return {}

@app.post("/video")
def post_item(video_data: VideoData):
    return {"video_id": encode_and_decode(video_data.video_path, video_data.codec)}

@app.get("/video/{video_id}")
def read_item(video_id: int):
    with PostgresAPI() as db:
        video_size, encoding_time, decoding_time = db.get_id(video_id)
    return {"video_size": video_size, "encoding_time": encoding_time, "decoding_time": decoding_time}

@app.delete("/video/{video_id}")
def read_item(video_id: int):
    with PostgresAPI() as db:
        db.delete_video(video_id)
    return {"video_id": video_id}