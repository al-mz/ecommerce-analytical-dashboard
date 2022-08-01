#!/bin/bash

# Initializes the Superset application
docker exec -ti -u root superset bash -c "sh ./docker-init.sh"

# Open the browser Superset
open http://localhost:8088

echo "Success! Login to Superset using the credentials admin/admin"