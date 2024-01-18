# hpc-net
Stateless, ethernet-based networking for datacenter-scale HPC applications.


## About
This repository contains PoCs for a set of networking protocols that use stateless, flow-zone-addressing enabled through software-defined-networks.


## Setup

### Step 1: Create Virtual Machine

- Download VMWare Workstation Player ([link](https://www.vmware.com/mena/products/workstation-player.html))
- Download the Ubuntu Server 20.04.6 LTS image ([link](https://releases.ubuntu.com/20.04.6/))
- Install VMWare and create a VM with at least 75 GBs of disk space and 4 GBs of RAM. Use the Ubuntu image downloaded earlier and install the OS to the VM.
- Run the next steps inside the VM.

### Step 2: Install P4, Mininet and their Dependencies

Run the following commands, in order;

```bash
git clone https://github.com/jafingerhut/p4-guide

# This script takes a long time to install (approx. 3+ hrs for me)
# and takes a lot of disk space, but is quite stable. You may try v5 of 
# the same script (in the same folder) which is much faster and takes 
# less space but is also less stable and may break some installations.
./p4-guide/bin/install-p4dev-v6.sh |& tee log.txt
```

The installation files will be present in the home directory and can be deleted after installation completes to free up disk space.

### Step 3: Install P4-Utils

The P4-Utils library makes it convenient to build and deploy p4 programs to switches in Mininet. To install, run the following commands, in order;

```bash
git clone https://github.com/nsg-ethz/p4-utils.git
cd p4-utils
sudo ./install.sh
```

**NOTE: DO NOT DELETE THE `p4-utils/` FOLDER IN THE HOME DIRECTORY AS THAT WILL BREAK YOUR INSTALLATION.**

### Step 4: Setup VSCode Server (Optional)

I recommend using VSCode's remote development plugin to make it more convenient to work in the VM. Instructions can easily be Googled.

### Step 5: Enable X11 Forwarding (Optional)

These are steps for Windows - not sure these will work (may not even be required) for other OSs.

- In Powershell run the following command:

    ```powershell
    setx DISPLAY "localhost:0"
    ```

- Install the VcXsrv Windows X Server ([link](https://sourceforge.net/projects/vcxsrv/)). Just install everything with the default selected options.
- In your ssh config file add the following lines to the profile;

    ```
    ForwardX11 yes
    ForwardX11Trusted yes
    ```

    Alternatively, you can also run ssh with the following command;
    ```powershell
    ssh -XY <username>@<vm_IP_address>
    ```
- Once inside the VM, the following command should print something;
    ```bash
    echo $DISPLAY
    # outputs "localhost:10.0" for me
    ```

- When running Mininet in the VM make sure to use `sudo -E`.

**Make sure to start VcXsrv manually before SSHing into the VM otherwise the X11 client won't connect to the display.**


## Usage

Check the `src/` folder for more usage instructions.