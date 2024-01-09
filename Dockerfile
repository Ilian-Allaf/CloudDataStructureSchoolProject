FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN wget https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20231010-093302/valeursfoncieres-2023.txt

COPY . /app/

EXPOSE 5000

ENV FLASK_APP=server.py

CMD ["flask", "run", "--host", "0.0.0.0"]
