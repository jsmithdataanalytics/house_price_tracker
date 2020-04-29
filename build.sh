sudo apt update && sudo apt upgrade
sudo apt install curl
sudo curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/download/v1.7.0/dbmate-linux-amd64
sudo chmod +x /usr/local/bin/dbmate || exit 1
sudo cp ./example.config.sh ./config.sh || exit 1
sudo chmod 777 ./config.sh
echo export AIRFLOW__CORE__FERNET_KEY=`python3 generate_fernet_key.py` | sudo tee -a ./config.sh || exit 1
source ./config.sh || exit 1
dbmate up || exit 1
echo "Success!"
