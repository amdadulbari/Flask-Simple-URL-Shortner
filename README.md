# Flask Simple URL Shortener

Flask Simple URL Shortener is a simple web application that allows users to shorten long URLs. It's built with Python Flask framework and uses Bootstrap for front-end design.

## Features
- login system.
- Short URL generation.
- Original and short URL storage.
- URL deletion.
- Copy short URL to clipboard.
![alt text](https://i.ibb.co/SVMZh52/flask-url-shortner-login.png "Login")

![alt text](https://i.ibb.co/jfXW44Q/flask-url-shortner-dashboard.png "Admin-Panel")

## Deploy

### Docker
To run the application using Docker, execute the following command:
```
docker build -t flask-simple-url-shortner .

docker run -d -p 5000:5000 -v $(pwd)/data/:/tmp/ --env-file=.env --name flask-simple-url-shortner flask-simple-url-shortner
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

