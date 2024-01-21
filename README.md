# Url Shortener Project

---

- Language: ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- Framework: ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
- Database: ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
  <br/><br/>
  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## How to run app

> To run the app you should follow this steps:

1. Install [**Docker**](https://docs.docker.com/get-docker/)
2. Go to the project directory
3. Type in terminal `sudo docker compose --env-file .env.prod up --build -d`

**Great! That's works!**

> Check [swagger of our app](http://localhost/docs)

**Next times you can run `sudo docker compose --env-file .env.prod up -d` to start server.**

**And `sudo docker compose stop` after you've finished working.**

**Also you can type `sudo docker compose down` to remove containers.**

## Run tests

> [Install Redis](https://redis.io/docs/install/install-redis/install-redis-on-linux/)

1. Stop running containers if there are any
2. Go to the project directory
3. Enter to poetry shell via `poetry shell`
4. Install deps `poetry install`
5. Run `./tests.sh`
