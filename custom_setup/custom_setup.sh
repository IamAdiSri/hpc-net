# Create a VM on VMWare Workstation and install Ubuntu Server 20.04 LTS from here: https://releases.ubuntu.com/20.04.6/
# Give the VM at least 50 GBs of hard disk space and 4 GBs of RAM. 

# Once the OS is installed, check its IP using the command: `ip address show`
# Use the IP to log in with VSCode - makes life easier. Copy your public key in ~/.ssh/authorized_keys to log in without
# having to use password.

# install zsh and oh-my-zsh
sudo apt-get install zsh
sudo chsh -s /usr/bin/zsh
# zsh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"
zsh custom_setup/ohmyzsh_install.sh

# install Miniconda (also comes with Python 3.11.5 at the time of writing)
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
zsh ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
# rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init zsh

# Use miniconda to create an env with the exact python version you plan on using (I picked 3.11.0 pretty randomly)
conda create -n ethairnet python=3.11
conda activate ethairnet

# install mininet
git clone https://github.com/mininet/mininet
# sudo mininet/util/install.sh -a
cp custom_setup/mininet_install.sh mininet/util/install.sh; sudo -E env "PATH=$PATH" mininet/util/install.sh -a

# install p4c (the P4 compiler)
source /etc/lsb-release
echo "deb http://download.opensuse.org/repositories/home:/p4lang/xUbuntu_${DISTRIB_RELEASE}/ /" | sudo tee /etc/apt/sources.list.d/home:p4lang.list
curl -fsSL "https://download.opensuse.org/repositories/home:p4lang/xUbuntu_${DISTRIB_RELEASE}/Release.key" | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_p4lang.gpg > /dev/null
sudo apt-get update
sudo -E env PATH="${PATH}" apt install p4lang-p4c

# install p4-bmv2 (the P4 BMv2 switch)
. /etc/os-release
echo "deb http://download.opensuse.org/repositories/home:/p4lang/xUbuntu_${VERSION_ID}/ /" | sudo tee /etc/apt/sources.list.d/home:p4lang.list
curl -fsSL "https://download.opensuse.org/repositories/home:p4lang/xUbuntu_${VERSION_ID}/Release.key" | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_p4lang.gpg > /dev/null
sudo apt update
sudo -E env PATH="${PATH}" apt install p4lang-bmv2
