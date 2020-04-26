# House Price Tracker
An Airflow pipeline that regularly scrapes asking prices from Zoopla and performs analytics

## Install
1. Clone the repo
2. Install dbmate: https://github.com/amacneil/dbmate
3. ```source ./config.sh```
4. ```pip install -r requirements.txt```
5. ```dbmate up```
6. ```airflow initdb```

## Run
1. ```airflow webserver -p 8080```
2. ```airflow scheduler```
3. In browser, turn on "house_price_tracker" DAG
