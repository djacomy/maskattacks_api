# Mask attack api

Docker contained project

## API

List of endpoints:

- De manière anonyme
  - POST /api/auth/signup - s'enroller
  - POST /api/auth/login - se connecter et recupperer un JWT tocker


- Avec authentification (Authorization: Bearer <JWT token>)
    - GET /api//user/<id>: Recupere un utilisateurs
    - PUT /api//user/<id>:  Modifie le profile d'un utilisateur
    - DELETE /api//user/<id>: Supprime un utilisateur 
    
    - GET /api/stocks: Récuperer la liste des stocks
    - GET /api/stocks/<id>: Récuperer un stock
    - PUT /api/stocks/<id>:  Modifier la quantite d'un stock
    
    - GET /api/request: liste des requetes
    - POST /api/requests: soumettre une requetes
    
    - GET /api/kits: Récuperer la liste des kits
    - GET /api/kits/<id>: Recupérer un kit
    - PUT /api/kits/<id>:  Modifier le statut d'un kit et/ou l'assinger a un transporteur
    
    - GET /api/protections: Recupere la liste des protections
    - GET /api/protections/<id>: Recupere une protection
    - PUT /api/protections/<id>:  Modifier le statut d'un protection et/ou l'assinger a un transporteur
    
    - GET /api/batches: Récuperer la liste des lots
    - POST /api/batches  params {"products":[1,2]): creer un batch a partir d'un liste de prouit de meme destination
    - GET /api/batches/<id>:  Récuperer lot
    - PUT /api/batches/<id>:  Modifier statut lot et/ou assigner lots.
    

## Installation

```
docker-compose run --rm server pip install -r requirements.txt --user --upgrade 
docker-compose up -d server
```

## Accessing containers

Require Docker >= 1.3

```shell
# use 'docker ps' to see the list of your containers
docker exec -it maskattacks_api_db_1 psql -Upostgres
docker exec -it maskattacks_api_db_server_1 bash
```

## Migration process

```shell
# Prior to the first migration
docker-compose run --rm server python src/manage.py db init

# Create a new version of the database
docker-compose run --rm server python src/manage.py db migrate
# check file + remove comment + improve file if needed
sudo vim migration/versions/<migration_id>.py

# Upgrade your database to the last version
docker-compose run --rm server python src/manage.py db upgrade
```

## Run tests

```shell
docker-compose run --rm testserver python -m unittest
```

## Commands

```shell
# Screenshot of python vendors
docker-compose run --rm server pip freeze > requirements.txt

# Run a command in the server container:
docker-compose run --rm server <command>
```
