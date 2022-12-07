#!/bin/bash

# Creates Olist PostgreSQL database
docker exec -it -u root ecommerce_analytics sh -c "conda run --no-capture-output -n ecom python ./examples/olist.py"

# Initializes the Superset application
docker exec -ti -u root superset bash -c "sh ./docker-init.sh"

# Open the browser Superset
open http://localhost:8088

echo "Success! Login to http://localhost:8088 using the defaul admin/admin credentials"