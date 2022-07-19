# The Ecommerce Dashboard
This is a supporting repo to create analyrical dashboard for the [Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) dataset by Kaggle. Current version provides a containarized platform to 
1. Automatically convert tabular data in csv format into PostgreSQL tables 
2. Create pre-defined materialized views for sales and their corresponding geolocation data.
3. Build a local Superset instance.

The visualizations are backed by open-source BI tool, [Apache-Superset](https://superset.apache.org/). Implementation is fully dockerized and can be reproduced in various environments. 

![2022-07-17 16-25-55 (5)](https://user-images.githubusercontent.com/59216368/179426482-de72b9de-8e2f-4c02-9787-1cc4459201de.gif)

# Dependecies
You need to install docker and docker-compose prior to running containers.


# Installation
1. Clone this repo:
```
$ git clone https://github.com/ali-mhmzadeh/ecommerce-analytical-dashboard.git
```

2. Start dockerized services. PostgreSQL will run on ports 5433, just in case you already have Postgres running: 
```
$ cd ecommerce-analytical-dashboard && docker-compose up
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

1. Login to http://localhost:8080/login/ with the following credentials and take a look:
```
username: admin
password: admin
```
## Create a quarterly sales chart by product line
2. Navigate to SQL Lab which provides a built-in SQL IDE. 

![2022-07-18 20-56-40](https://user-images.githubusercontent.com/59216368/179642702-f7e3494a-2ff7-4c26-adcc-ef5c9a04292d.gif)

3. Write your select query against the provided view and select on "create chart". 
```
SELECT *
FROM dbview_schema.cleaned_sales_data 
```

4. Create the time-series bar chart.


![2022-07-18 21-34-08 (1)](https://user-images.githubusercontent.com/59216368/179645715-1d4d4cf7-9135-451b-8f8a-32ce930ac109.gif)






