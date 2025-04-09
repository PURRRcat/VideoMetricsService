import gi
import os
gi.require_version('Gst', '1.0')
from gi.repository import Gst

def encode_video(input_path, output_path, codec):

    if (not os.path.exists(input_path) or
            not codec in ["x264enc", "x265enc", "vp9enc", "av1enc"]):
        return -1

    Gst.init(None)
    # print("Версия:", Gst.version_string())

    # в зависимости от кодека нужно будет формат выходного видео править
    pipeline_str = (
        f"filesrc location={input_path} ! decodebin name=dec "
        f"dec. ! {codec} ! mp4mux name=mux ! filesink location={output_path} "
        # f"dec. ! audioconvert ! audioresample ! lamemp3enc ! mux." # для аудио свои приколы
    )

    pipeline = Gst.parse_launch(pipeline_str)

    pipeline.set_state(Gst.State.PLAYING)
    bus = pipeline.get_bus()

    bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS)

    running_time = pipeline.get_current_running_time() / Gst.SECOND

    pipeline.set_state(Gst.State.NULL)


    return running_time

print (encode_video("../videos/sample.mp4", "../videos/out_sample.mp4", "x264enc"))