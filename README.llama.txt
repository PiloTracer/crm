docker pull ollama/ollama

docker run -d -v ollama:/root/.ollama --network simple_web --ip 10.5.0.9 -p 11434:11434 --name ollama ollama/ollama

docker exec -it ollama ollama pull codellama

docker exec -it ollama ollama run codellama

docker exec -it ollama ollama run mistral

docker exec -it ollama ollama run llama2

docker exec -it ollama ollama run llama2:70b

ollama run llama2:70b

ollama pull mistral

docker exec -it ollama ollama

docker exec -it ollama ollama pull mistral


docker run -d -v ollama:/root/.ollama --network simple_web --ip 10.5.0.9 -p 11434:11434 --name ollama ollama/ollama

docker exec -it ollama ollama run llama2
 docker run -it --network simple_web --ip 10.5.0.6 -p 8000:8000 fastap_i /bin/sh