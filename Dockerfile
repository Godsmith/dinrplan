ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel

RUN mkdir -p /app
WORKDIR /app

COPY . .

# Even though we use hatch locally, we have to use the system python in the Dockerfile
# for it to work on fly.io for some reason.
RUN pip install hatch
RUN hatch dep show requirements > requirements.txt
RUN pip install -r requirements.txt

# These environment variables are needed for collectstatic to run, but they are stored
# in secrets in fly.io which are not available during the build process. So just set
# them to non-empty strings in the meantime.
ARG SECRET_KEY=dummy
ARG DATABASE_URL=dummy
RUN python manage.py collectstatic --noinput


EXPOSE 8080

CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "dinrplan.wsgi"]
