# Python `Flask` API Basics

Projects based on the Udemy course [Python REST APIs with Flask, Docker, MongoDB, and AWS DevOps](https://www.udemy.com/course/python-rest-apis-with-flask-docker-mongodb-and-aws-devops).  


The repo's contents generally follow the project curriculum with modifications made to certain projects; different packages used, additional functionality added, more documentation, etc.

**[project-hello-world](project-hello-world/)**
- Implements a basic REST API
- New tech, concepts, relative to any previous project(s) in the course:
  - REST API basics: GET and POST methods, JSON, client/server request/response processes
  - Postman
  - `Flask` package
  - Python virtual environments
  - Environment variables

**[project-restful-calculator](project-restful-calculator/)**
- Implements a simple alculator API
- Tracks number of calcs done in a NoSQL database and handles simple operations (+ - * /)
- New tech, concepts, relative to any previous project(s) in the course:
  - NoSQL databases. Used `MongoDB` for this project
  - `Flask-RESTful` package
  - Microservices
  - Docker Compose to manage microservices

**[project-DatabaseAAS-restful-api](project-DatabaseAAS-restful-api/)**
- Implement a _database as a service_ API.
- Allows a user to register for the service, store data (a single sentence) for a fee, manage/view their fee credits balance, and retrieve their stored data.
- Makes use of these additional technologies: updated version of MongoDB, removed
- New tech, concepts, relative to any previous project(s) in the course:
  - Updated version and syntax for MongoDB
  - Resolve dependency issue by removing `Flask-RESTful` since it was incompatible with updated MongoDB and Docker versions. Used only `Flask` instead
  - Safe password storage via hashing with `bcrypt`.
  - Dynamically updating NoSQL documents based on user input.