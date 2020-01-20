docker system prune

docker volume rm $(docker volume ls)

docker rm $(docker container ps -q) --force

docker rmi $(docker images -q) --force 