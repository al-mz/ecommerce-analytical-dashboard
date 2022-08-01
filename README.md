# The Ecommerce Dashboard
This is a supporting repo to create analyrical dashboard for the [Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) dataset by Kaggle. Current version provides a containarized platform to:  
1. Build a PostgreSQL database with Olist Ecommerce datasets. 
2. Create materialized views for sales and geolocation data.
3. Build and initialize a local Superset instance with default username and password
4. Import a pre-made dashboard named Olist. 

The visualizations are backed by the open-source BI tool, [Apache-Superset](https://superset.apache.org/). Implementation is fully dockerized and can be reproduced in various environments. 

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

## Initialize Superset App
3. After the Docker containers have started and are running, you'll need to bootstrap the cluster to initialize Superset app and dashboard. The following command will connect Superset to the Olist database and import pre-made dashboard:

```
$ sh boostrap.sh
```

# Quick start

1. Login to http://localhost:8080/login/ with the following credentials and take a look:
```
username: admin
password: admin
```

2. Navigate to the Dashboards and take a look at the olist dashboard. 






