from fastapi import FastAPI
from pydantic import BaseModel
from gstreamer import encode_and_decode

app = FastAPI()

class VideoData(BaseModel):
    video_path: str
    codec: str

# @app.get("/")
# def read_root():
#     return {}

@app.post("/video")
def post_item(video_data: VideoData):
    # encode_video(video_data.video_path, video_data.codec)
    encode_and_decode()
    return {"video_id": video_data}

@app.get("/video/{video_id}")
def read_item(video_id: int):

    return {"video_id": video_id}

@app.delete("/video/{video_id}")
def read_item(video_id: int):
    return {"video_id": video_id}