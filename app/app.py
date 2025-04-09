from fastapi import FastAPI
from pydantic import BaseModel
from gstreamer import encode_video

app = FastAPI()

class VideoData(BaseModel):
    video_path: str
    codec: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/video")
def post_item(video_data: VideoData):
    return {"video_id": video_data}

@app.get("/video/{video_id}")
def read_item(video_id: int):
    return {"video_id": video_id}

@app.delete("/video/{video_id}")
def read_item(video_id: int):
    return {"video_id": video_id}