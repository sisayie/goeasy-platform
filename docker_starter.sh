echo Kill all docker processes
docker-compose rm -fs

echo Remove all docker images
docker rmi $(docker images -q) --force

echo building docker containers
docker-compose up --build -d
