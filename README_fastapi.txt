############swager:
http://localhost:8000/docs#/default/index__get

run it manually:
docker run -d -v fastap_i --network simple_web --ip 10.5.0.6 -p 8000:8000

docker run -it --network simple_web --ip 10.5.0.6 -p 8000:8000 fastap_i