echo "---------------Building auth-service docker image--------------------"
docker build -t auth-service .
echo "---------------Building docker image done----------------------------"
echo "---------------Running the auth-service container--------------------"
container_id=$(docker run -d -p 3000:3000 auth-service)
echo "---------------Container started successfully------------------------"
echo "Container ID: $container_id"
echo "---------------auth-service listening on port 3000------"