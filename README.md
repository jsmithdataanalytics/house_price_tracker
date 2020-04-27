# House Price Tracker
An Airflow pipeline that regularly scrapes asking prices from Zoopla and performs analytics

## Install
1. Clone the repo
2. ```pip install -r requirements.txt```
3. ```source ./build.sh```

## Run locally
1. In one shell: ```source ./config.sh && airflow webserver -p 8080```
2. In another: ```source ./config.sh && airflow scheduler```
3. In browser, go to Admin > Connections
4. Create connection "sender_email" with host, port, login, password
5. Under "extra" section, enter ```{"recipients": ["example1@gmail.com", "example2@hotmail.com"]}```
6. Turn on "house_price_tracker" DAG
