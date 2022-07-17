# The Ecommerce Dashboard
This is a supporting dashboard for the [Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) dataset provided by Kaggle. It provides an overview of sales at different timeframes. The dashboard is built with open-source[Apache-Superset](https://superset.apache.org/) BI tool using pre-defined Postgres views. It is fully dockerized and can be reproduced in various environments. 

![2022-07-17 16-25-55 (5)](https://user-images.githubusercontent.com/59216368/179426482-de72b9de-8e2f-4c02-9787-1cc4459201de.gif)

# Dependecies
- Docker
- Docker-compose


# Usage
clone the repository and then run
```
cd ecommerce-analytics
docker-compose up
```
In the background, it will generate three containers, including PostgreSQL, Superset and one for creating sales view. 




