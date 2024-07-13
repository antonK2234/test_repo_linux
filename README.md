!sudo apt update
!sudo apt upgrade
!sudo apt install sagemath

!sudo apt install -y software-properties-common
!sudo add-apt-repository ppa:deadsnakes/ppa
!sudo apt update

!sudo apt install -y python3.9 python3.9-venv python3.9-dev
!sudo apt install -y python3-pip
!pip3 install requests~=2.32.3
!pip3 install bitcoin~=1.1.42
!pip3 install colorama~=0.4.6
!pip3 install cryptography
!sage -pip install bitcoin --break-system-packages

!lsb_release -a
!python3 --version
!pip3 --version
!sage --version

!sage -python3 LLL-Atack-by-focus-v5.py

----------------------
sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl libbz2-dev


cd /usr/src
sudo wget https://www.python.org/ftp/python/3.11.4/Python-3.11.4.tgz
sudo tar xzf Python-3.11.4.tgz


cd Python-3.11.4
sudo ./configure --enable-optimizations
sudo make altinstall

