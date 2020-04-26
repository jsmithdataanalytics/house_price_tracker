# House Price Tracker
An Airflow pipeline that regularly scrapes asking prices from Zoopla and performs analytics

## Installation
1. Clone the repo
2. From the root of the repo: ```source ./build.sh```
3. ```airflow webserver -p 8080```
4. ```airflow scheduler```