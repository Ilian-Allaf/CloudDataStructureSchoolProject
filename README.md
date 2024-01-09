# Run MongoDB container
```bash
docker compose up -d
```

# Download Data by copying this link in your browser

```
https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20231010-093302/valeursfoncieres-2023.txt
```

Move it in the root project directory

# Insert data in MongoDB

```bash
python insertdata.py
```

# Run queries

```bash
python queries.py
```
