echo "ProjectARGS Official Installer"

sudo pacman -S python python-pip sqlite mongodb

sudo pip install pymongo
sudo pip install tqdm
sudo pip install intervaltree
sudo pip install sqlitebck

sudo mkdir /data
sudo mkdir /data/db
