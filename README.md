# The Ecommerce Dashboard
This is a supporting dashboard for the [Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) dataset by Kaggle. In current version, it provides an overview of sales at different timeframes. The dashboard is built with open-source[Apache-Superset](https://superset.apache.org/) BI tool using pre-defined Postgres views. It is fully dockerized and can be reproduced in various environments. 

# Dependecies
- Docker
- Docker-compose


# Installation
1. Clone the repository
2. Createdocker contaienrs
```
$ cd ecommerce-analytics
$ docker-compose up
```

3. Initialize a local Superset Instance
- Setup your local admin account
```
$ docker exec -it superset superset fab create-admin\
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password admin
```

4. Migrate local DB to latest
```
$ docker exec -it superset superset db upgrade
```
5. Load examples (optional)
```
$ docker exec -it superset superset load_examples
```
6. Set up roles
```
$ docker exec -it superset superset init
```
7. Login and take a look -- navigate to http://localhost:8080/login/ -- u/p: [admin/admin]






