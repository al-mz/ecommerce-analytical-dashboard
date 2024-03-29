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

STEP_CNT=6

echo_step() {
cat <<EOF
######################################################################
Init Step ${1}/${STEP_CNT} [${2}] -- ${3}
######################################################################
EOF
}

# Create an admin user
echo_step "1" "Starting" "Setting up admin user ( admin / admin )"
superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password admin
echo_step "1" "Complete" "Setting up admin user"

# Initialize the database
echo_step "2" "Starting" "Applying DB migrations"
superset db upgrade
echo_step "2" "Complete" "Applying DB migrations"

# Create default roles and permissions
echo_step "4" "Starting" "Setting up roles and perms"
superset init
echo_step "4" "Complete" "Setting up roles and perms"

# Import Olist dashboards
echo_step "6" "Starting" "Importing the Olist dashboard"
superset import-dashboards -p ./olist-dashboard.zip
echo_step "6" "Complete" "Importing the Olist dashboard"

# Update Olist database connection URI
echo_step "6" "Starting" "Updating Olist database connection URI"
superset set_database_uri -d olist-quickstart -u postgresql://postgres:password@db:5432/ecommerce_analytics
echo_step "6" "Complete" "Updating Olist database connection URI"