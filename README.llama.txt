docker pull ollama/ollama

docker run -d -v ollama:/root/.ollama --network simple_web --ip 10.5.0.9 -p 11434:11434 --name ollama ollama/ollama

docker exec -it ollama ollama pull codellama

docker exec -it ollama ollama run codellama


docker exec -it ollama ollama run llama2

ollama pull mistral

docker exec -it ollama ollama

docker exec -it ollama ollama pull mistral