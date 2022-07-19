# The Ecommerce Dashboard
This is a supporting dashboard for the [Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) dataset by Kaggle. In current version, it provides an overview of sales at different timeframes. The dashboard is built with open-source[Apache-Superset](https://superset.apache.org/) BI tool using pre-defined Postgres views. It is fully dockerized and can be reproduced in various environments. 

![2022-07-17 16-25-55 (5)](https://user-images.githubusercontent.com/59216368/179426482-de72b9de-8e2f-4c02-9787-1cc4459201de.gif)

# Dependecies
You need to install docker and docker-compose in order to create containers.


# Installation
1. Clone this repo:
```
$ git clone https://github.com/ali-mhmzadeh/ecommerce-analytical-dashboard.git
```

2. Start dockerized services. PostgreSQL and Superset will run on ports 5433 just in case you already have Postgres running: 
```
$ cd ecommerce-analytics && docker-compose up
```

## Initialize a local Superset Instance
3. Setup your local admin account
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

# Quick start

Login into http://localhost:8080/login/ using the following credentials:
```
username: admin
password: admin
```






