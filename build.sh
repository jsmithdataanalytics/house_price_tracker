sudo apt update && sudo apt upgrade
sudo apt install curl
sudo curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/download/v1.7.0/dbmate-linux-amd64
sudo chmod +x /usr/local/bin/dbmate
source venv/bin/activate
pip install -r requirements.txt
sudo cp ./example.config.sh ./config.sh
sudo chmod 777 ./config.sh
echo export AIRFLOW__CORE__FERNET_KEY=`python3 generate_fernet_key.py` | sudo tee -a ./config.sh
source ./config.sh
dbmate up
airflow initdb
