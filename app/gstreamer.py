import gi
import os
gi.require_version('Gst', '1.0')
from gi.repository import Gst
from postgresql import PostgresAPI

def encode_and_decode(input_path = "/videos/sample.mp4", codec = "x264enc"):

    if (not os.path.exists(input_path) or
            not codec in ["x264enc", "x265enc", "vp9enc", "av1enc"]):
        return -1

    Gst.init(None)

    pipeline_encoding = (
        f"filesrc location={input_path} ! decodebin "
        f"! {codec} ! mp4mux ! filesink location=/videos/encoded "
    )
    pipeline_decoding = (
        f"filesrc location=/videos/encoded ! decodebin ! filesink location=/videos/output.mp4"
    )

    pipeline = Gst.parse_launch(pipeline_encoding)
    pipeline.set_state(Gst.State.PLAYING)
    bus = pipeline.get_bus()
    bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS)
    encoding_time = pipeline.get_current_running_time() / Gst.SECOND
    pipeline.set_state(Gst.State.NULL)

    file_size = os.path.getsize("/videos/encoded")

    pipeline = Gst.parse_launch(pipeline_decoding)
    pipeline.set_state(Gst.State.PLAYING)
    bus = pipeline.get_bus()
    bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS)
    decoding_time = pipeline.get_current_running_time() / Gst.SECOND
    pipeline.set_state(Gst.State.NULL)

    print(file_size, encoding_time, decoding_time)
    with PostgresAPI() as db:
        return db.insert(file_size, encoding_time, decoding_time)


# print (encode_video("../videos/sample.mp4", "../videos/out_sample.mp4", "x264enc"))