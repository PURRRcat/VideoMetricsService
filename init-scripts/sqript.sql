CREATE TYPE status_type AS ENUM ('new', 'in_progress', 'done', 'error');

CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    video_size FLOAT,
    encoding_time FLOAT,
    decoding_time FLOAT,
    status status_type DEFAULT 'new'
);
