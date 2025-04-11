import gi
import os
gi.require_version('Gst', '1.0')
from gi.repository import Gst
from postgresql import PostgresAPI

out_name = {
    "AV1": "output_av1.webm",
    "H.264": "output_h264.mp4",
    "H.265": "output_h265.mp4",
    "VP9": "output_vp9.webm",
    "RAW": "output.raw"
}
params = {
    "AV1": "av1enc cpu-used=8 ! webmmux", # не запускайте _)
    "H.264": "x264enc ! mp4mux",
    "H.265": "x265enc ! h265parse ! mp4mux",
    "VP9": "vp9enc cpu-used=8 ! webmmux", # оно того не стоит
    "RAW": "videoconvert ! video/x-raw,format=YV12"
}

def get_time(pipeline_str):
    pipeline = Gst.parse_launch(pipeline_str)
    pipeline.set_state(Gst.State.PLAYING)
    bus = pipeline.get_bus()
    bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS)
    encoding_time = pipeline.get_current_running_time() / Gst.SECOND
    pipeline.set_state(Gst.State.NULL)
    return encoding_time



def encode_and_decode(video_id, input_path = "sample.mp4", codec = "H.264"):

    for video in input_path:
        if (not os.path.exists(f"/videos/{video}") or
            not codec in out_name.keys()):
            return f"videos/{input_path}"

    Gst.init(None)

    pipeline_encoding = f"concat name=c ! {params[codec]} ! filesink location=/videos/{out_name[codec]} "

    for video in input_path:
        pipeline_encoding += f"filesrc location=/videos/{video} ! decodebin ! c. "

    print(pipeline_encoding)

    if codec != "RAW":
        pipeline_decoding = (
            f"filesrc location=/videos/{out_name[codec]} ! decodebin ! videoconvert ! fakesink"
        )
    else:
        pipeline_decoding = (
            f"filesrc location=/videos/{out_name[codec]} ! decodebin ! videoconvert ! fakesink"
        )

    with PostgresAPI() as db:
        db.insert_status('in_progress', video_id)
    encoding_time = get_time(pipeline_encoding)
    file_size = os.path.getsize(f"/videos/{out_name[codec]}") / (1024 * 1024)
    decoding_time = get_time(pipeline_decoding)

    with PostgresAPI() as db:
        db.insert_values(file_size, encoding_time, decoding_time, video_id)
        db.insert_status("done", video_id)