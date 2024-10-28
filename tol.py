# dino_injector.py
import os
import requests
import string
import itertools
import time
import threading
from colorama import Fore, Style

os.system("clear")
print(f"{Fore.RED} ____  _   _ ____   ____ ____  _  __  ")
print(f"{Fore.RED}/ ___|| | | |  _ \ / ___|  _ \| |/ /  ")
print(f"{Fore.RED}\___ \| | | | |_) | |   | | | | ' /   ")
print(f"{Fore.RED} ___) | |_| |  _ <| |   | |_| | . \   ")
print(f"{Fore.RED}|____/ \___/|_| \_\\_|   |____/|_|\_\ ")
url = input(f"{Fore.MAGENTA}Enter the target URL: {Fore.CYAN}")
words = input(f"{Fore.MAGENTA}Enter the words to inject: {Fore.CYAN}")

payload = {
    "vuln_field": f"<dino>{words}</dino>"
}

directories = []
min_length = 1
max_length = 8

total_combinations = sum(len(string.ascii_lowercase) ** i for i in range(min_length, max_length + 1))
completed_combinations = 0
start_time = time.time()

stop_attack = False

def check_for_enter_press():
    nonlocal stop_attack
    input()
    stop_attack = True

enter_thread = threading.Thread(target=check_for_enter_press)
enter_thread.start()

for combination in itertools.product(string.ascii_lowercase, repeat=min_length):
    if stop_attack:
        break

    directory = ''.join(combination)
    exploit_url = url + directory
    if try_exploit(exploit_url, payload):
        directories.append(directory)

    completed_combinations += 1
    progress = (completed_combinations / total_combinations) * 100

    elapsed_time = time.time() - start_time
    average_time_per_combination = elapsed_time / completed_combinations
    remaining_combinations = total_combinations - completed_combinations
    estimated_time = average_time_per_combination * remaining_combinations

    os.system("clear")
    print(f"{Fore.RED} ____  _   _ ____   ____ ____  _  __  ")
    print(f"{Fore.RED}/ ___|| | | |  _ \ / ___|  _ \| |/ /  ")
    print(f"{Fore.RED}\___ \| | | | |_) | |   | | | | ' /   ")
    print(f"{Fore.RED} ___) | |_| |  _ <| |   | |_| | . \   ")
    print(f"{Fore.RED}|____/ \___/|_| \_\\_|   |____/|_|\_\ ")
    print(f"{Fore.CYAN}Progress: {Fore.RED}[{'=' * int(progress / 2)}{Fore.RED}{' ' * (50 - int(progress / 2))}{Fore.RED}] {Fore.CYAN}{progress:.2f}%{' ' * 10}")
    print(f"{Fore.CYAN}Estimated Time: {Fore.YELLOW}{time.strftime('%H:%M:%S', time.gmtime(estimated_time))}")
    print(f"{Fore.YELLOW}Please press ENTER to stop the attack{Style.RESET_ALL}")

os.system("clear")
print(f"{Fore.RED} ____  _   _ ____   ____ ____  _  __  ")

print(f"{Fore.RED}/ ___|| | | |  _ \ / ___|  _ \| |/ /  ")
print(f"{Fore.RED}\___ \| | | | |_) | |   | | | | ' /   ")
print(f"{Fore.RED} ___) | |_| |  _ <| |   | |_| | . \   ")
print(f"{Fore.RED}|____/ \___/|_| \_\\_|   |____/|_|\_\ ")
if directories:
    print(f"{Fore.GREEN}Discovered directories ('{words}' injected):")
    for directory in directories:
        print(f"{Fore.GREEN}- {directory}")
else:
    print(f"{Fore.RED}No vulnerable directories found.{Style.RESET_ALL}")

if directories:
    inject_again = input(f"{Fore.MAGENTA}Continue with injection in discovered directories? (y/n): {Fore.CYAN}")
    if inject_again.lower() == 'y':
        for directory in directories:
            inject_words(url + directory, words)
