# House Price Tracker
An Airflow pipeline that regularly scrapes asking prices from Zoopla and performs analytics

## Install
1. Clone the repo
2. ```source ./build.sh```

## Run
1. In one tmux session: ```airflow webserver -p 8080```
2. In another: ```airflow scheduler```
3. In browser, go to Admin > Connections
4. Create connection "sender_email" with host, port, login, password
5. Turn on "house_price_tracker" DAG
