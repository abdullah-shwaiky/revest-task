FROM python:3.10-slim

WORKDIR /dockerRecommender

COPY ./requirements.txt /dockerRecommender/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /dockerRecommender/
RUN chmod +x ./wait-for-it.sh
RUN chmod +x ./init.sh

EXPOSE 8000

ENTRYPOINT ["/wait-for-it.sh", "postgres:5432", "--", "./init.sh"]
