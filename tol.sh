#!/bin/bash

# Install required packages
pkg update && pkg upgrade -y
pkg install wget proot -y

# Download and install Kali Linux
wget https://raw.githubusercontent.com/EXALAB/AnLinux-Resources/master/Scripts/Shell/Apt/kali.sh
bash kali.sh

# Set up rainbow loading bar
Loading() {
    echo -e "\033[31m*\033[0m\c"
    sleep 0.1
    echo -e "\b\033[32m*\033[0m\c"
    sleep 0.1
    echo -e "\b\033[33m*\033[0m\c"
    sleep 0.1
    echo -e "\b\033[34m*\033[0m\c"
    sleep 0.1
    echo -e "\b\033[35m*\033[0m\c"
    sleep 0.1
    echo -e "\b\033[36m*\033[0m\c"
    sleep 0.1
    echo -e "\b\033[37m*\033[0m\c"
    sleep 0.1
}

# Create aliases for switching environments
echo "alias kali='proot -0 -r ~/anlinux-files/kali-root -b /usr/bin/env -l -c ~/.anlinux-scripts/kali-root/login.sh'" >> ~/../usr/etc/bash.bashrc
echo "alias termux='exit'" >> ~/anlinux-scripts/kali-root/login.sh

# Display loading bar
echo -e "\nSetting up Kali Linux environment..."
for i in {1..10}; do
    Loading
done
echo -e "\nKali Linux environment setup complete!"

# Clean up
rm kali.sh

echo -e "\nInstallation finished. You can now switch to Kali Linux by typing 'kali' and switch back to Termux by typing 'termux'."
