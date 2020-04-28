# House Price Tracker
An Airflow pipeline that regularly scrapes asking prices from Zoopla and performs analytics

## Install
1. Clone the repo
2. ```pip install -r requirements.txt```
3. ```source ./build.sh```

## Run
1. ```source ./config.sh && airflow webserver -p 8080```
2. ```source ./config.sh && airflow scheduler```
3. In Airflow web UI, go to Admin > Connections
4. Create connection "sender_email" with host, port, login, password
5. Under "extra" section, specify email recipients: ```{"recipients": ["example1@gmail.com"]}```
6. Turn on "house_price_tracker" DAG
