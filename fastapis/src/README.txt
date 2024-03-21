Swager:
http://localhost:8000/docs#/default/index__get


Ollama:
1) docker run -d -v ollama:/root/.ollama --network simple_web --ip 10.5.0.9 -p 11434:11434 --name ollama ollama/ollama
2) docker exec -it ollama ollama run llama2
3) install other models:  docker exec -it ollama ollama pull mistral
