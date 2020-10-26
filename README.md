sudo apt install python3-venv
python3 -m venv venv_autoclean
source venv_autoclean/bin/activate

pip3 install django requests

apt-get install libxml2-dev libxslt1-dev python-dev
pip3 install -r requirements.txt
##VUE##
sudo apt install nodejs npm
npm install -g @vue/cli
vue create vue_autoclean

cd vue_autoclean
npm run serve
so