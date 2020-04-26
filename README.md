# House Price Tracker
An Airflow pipeline that regularly scrapes asking prices from Zoopla and performs analytics

## Installation
1. Clone the repo
2. Install dbmate: https://github.com/amacneil/dbmate
3. ```source ./config.sh```
4. ```pip install -r requirements.txt```
5. ```dbmate up```
6. ```airflow initdb```
7. ```airflow webserver -p 8080```
8. ```airflow scheduler```
9. In browser, turn on "house_price_tracker" DAG
