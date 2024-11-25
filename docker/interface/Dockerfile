FROM python:3.10-slim

WORKDIR /dockerInterface

COPY ./requirements.txt /dockerInterface/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /dockerInterface/
RUN chmod +x ./wait-for-it.sh
RUN chmod +x ./init.sh

EXPOSE 8500

ENTRYPOINT ["/wait-for-it.sh", "postgres:5432", "--", "./init.sh"]
