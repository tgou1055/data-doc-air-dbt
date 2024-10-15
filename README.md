
## Environment Setup (Ubuntu WSL)

sudo apt update
sudo apt install python3
sudo apt install python3-pip

sudo apt install pipenv

which python3 (get <PYTHON3_PATH>)

pipenv shell --python <PYTHON3_PATH>
pipenv install awscli
pipenv install boto3
pipenv install pandas
pipenv install jupyter

### To open jupyter
jupyter notebook --no-browser --ip=0.0.0.0 --port=8888