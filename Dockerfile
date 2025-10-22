FROM python:3.12-slim AS base
WORKDIR /workdir

# install dependencies
RUN mkdir /workdir/tmp
COPY requirements.txt /workdir/tmp/requirements.txt
RUN pip install -r /workdir/tmp/requirements.txt
COPY app /workdir/app
COPY Util /workdir/Util
COPY Dao /workdir/Dao
RUN rm -rf /workdir/tmp
ENV PYTHONPATH=/workdir
# for Chinese Users: -i https://pypi.tuna.tsinghua.edu.cn/simple

# build apps, check path for each app (workdir/app)
# build app Index
FROM base AS Index
EXPOSE 8000
CMD ["python", "-m", "app.Index"]
#  build app Game
FROM base AS Game
EXPOSE 8010
CMD ["python", "-m", "app.Game"]
#  build app StyleSheet
FROM base AS StyleSheet
EXPOSE 8020
CMD ["python", "-m", "app.StyleSheet"]

# Docker-compose is ready for usage
# UP: $ docker compose up --build -d
# DOWN: $ docker compose down
# Check logs: $ docker compose logs -f (--tail=100)