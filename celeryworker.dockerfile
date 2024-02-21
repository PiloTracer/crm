FROM python:3.12

RUN pip install raven celery passlib[bcrypt]==1.7.4 cloudant==2.15.0 tenacity==8.2.2

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter notebook --ip=0.0.0.0 --allow-root
ARG env=prod
RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyter ; fi"
EXPOSE 8888

ENV C_FORCE_ROOT=1

WORKDIR /code
COPY ./backend/app ./app

ENV PYTHONPATH=/app

COPY ./backend/worker-start.sh ./worker-start.sh

RUN chmod +x ./worker-start.sh

CMD ["bash", "./worker-start.sh"]
