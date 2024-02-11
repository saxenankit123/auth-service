echo "---------------Building docker image--------------------"
docker build -t auth-service .
echo "---------------Building docker image done--------------------"
echo "---------------Running the container--------------------"
docker run -d -p 3000:3000 auth-service
echo "---------------auth-service listening on port 3000--------------------"