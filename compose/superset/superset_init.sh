#!/usr/bin/env bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
set -e

#
# Always install local overrides first
#
# /app/docker/docker-bootstrap.sh

STEP_CNT=4

echo_step() {
cat <<EOF

######################################################################


Init Step ${1}/${STEP_CNT} [${2}] -- ${3}


######################################################################

EOF
}

# Initialize the step number variable
STEP_NUMBER=1

# Applying DB migrations
echo_step "$STEP_NUMBER" "Starting" "Applying DB migrations"
superset db upgrade
echo_step "$STEP_NUMBER" "Complete" "Applying DB migrations"
STEP_NUMBER=$((STEP_NUMBER + 1))

# Create default roles and permissions
echo_step "$STEP_NUMBER" "Starting" "Setting up roles and perms"
superset init
echo_step "$STEP_NUMBER" "Complete" "Setting up roles and perms"
STEP_NUMBER=$((STEP_NUMBER + 1))

# Create an admin user
echo_step "$STEP_NUMBER" "Starting" "Setting up admin user ( "$ADMIN_USERNAME" / $ADMIN_PASSWORD )"
superset fab create-admin \
--username "$ADMIN_USERNAME" \
--firstname Superset \
--lastname Admin \
--email "$ADMIN_EMAIL" \
--password "$ADMIN_PASSWORD"
echo_step "$STEP_NUMBER" "Complete" "Setting up admin user"
STEP_NUMBER=$((STEP_NUMBER + 1))

# Update Olist database connection URI
echo_step "6" "Starting" "Updating Olist database connection URI"
superset set_database_uri -d olist-quickstart -u postgresql://postgres:password@db:5432/ecommerce_analytics
echo_step "6" "Complete" "Updating Olist database connection URI"

# Load examples if SUPERSET_LOAD_EXAMPLES is set True
if [ "$SUPERSET_LOAD_EXAMPLES" = "True" ]; then
    echo_step "$STEP_NUMBER" "Starting" "Loading examples"
    superset load_examples --force
    echo_step "$STEP_NUMBER" "Complete" "Loading examples"
    STEP_NUMBER=$((STEP_NUMBER + 1))
fi

# Import Olist dashboards
echo_step "6" "Starting" "Importing the Olist dashboard"
superset import-dashboards -p ./olist-dashboard.zip -u "$ADMIN_USERNAME"
echo_step "6" "Complete" "Importing the Olist dashboard"

# Starting server with Gunicorn
echo "Starting server with Gunicorn"
gunicorn \
    -w 10 \
    -k gevent \
    --worker-connections 1000 \
    --timeout 120 \
    -b 0.0.0.0:8088 \
    --limit-request-line 0 \
    --limit-request-field_size 0 \
    "superset.app:create_app()"