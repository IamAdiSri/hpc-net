# Create a VM on VMWare Workstation and install Ubuntu Server 20.04 LTS from here: https://releases.ubuntu.com/20.04.6/
# Give the VM at least 75 GBs of hard disk space and 4 GBs of RAM. 

# Once the OS is installed, check its IP using the command: `ip address show`
# Use the IP to log in with VSCode - makes life easier. Copy your public key in ~/.ssh/authorized_keys to log in without
# having to use password.

# Install mininet, p4 and all dependencies
# Read more here: https://github.com/jafingerhut/p4-guide/blob/master/bin/README-install-troubleshooting.md
git clone https://github.com/jafingerhut/p4-guide
# ./p4-guide/bin/install-p4dev-v5.sh |& tee log.txt # takes very little time and space but less stable
./p4-guide/bin/install-p4dev-v6.sh |& tee log.txt # large time and space requirement but is more stable 

# Install p4-utils (dependencies were already installed in previous step)
# Read more here: https://github.com/nsg-ethz/p4-utils#manual-installation
# NOTE: Don't delete the p4-utils folder after installing
git clone https://github.com/nsg-ethz/p4-utils.git
cd p4-utils
sudo ./install.sh

# install zsh and oh-my-zsh
sudo apt-get install zsh
sudo chsh -s /usr/bin/zsh
# zsh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"
zsh custom_setup/ohmyzsh_install.sh
