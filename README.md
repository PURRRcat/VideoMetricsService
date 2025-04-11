Build and run:

docker-compose up --build



Example curl requests:

POST
curl -X POST http://0.0.0.0:80/video \
-H "Content-Type: application/json" \
-d '{"video_path": "sample.mp4", "codec": "H264"}'

GET
curl http://0.0.0.0:80/video/1

DELETE
curl -X DELETE http://0.0.0.0:80/video/1



Available codecs:

H.264, H.265, VP9(, AV1)
