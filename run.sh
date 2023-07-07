docker rm -f flask-simple-url-shortner
docker build -t flask-simple-url-shortner .
docker run -d -p 5000:5000 -v $(pwd)/data/:/tmp/ --env-file=.env --name flask-simple-url-shortner flask-simple-url-shortner
