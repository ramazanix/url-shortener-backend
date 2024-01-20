FROM python:3.10 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10
WORKDIR /url-shortener
COPY --from=requirements-stage /tmp/requirements.txt /url-shortener/requirements.txt
COPY .env.prod /url-shortener/.env
RUN pip install --no-cache-dir --upgrade -r /url-shortener/requirements.txt
COPY ./src /url-shortener/src
COPY ./alembic.ini /url-shortener/alembic.ini
COPY ./alembic /url-shortener/alembic

RUN chmod +x /url-shortener/alembic/apply_migrations.sh
ENTRYPOINT ["/url-shortener/alembic/apply_migrations.sh"]
CMD python -m uvicorn src:init_app --host 0.0.0.0 --port 80 --factory
