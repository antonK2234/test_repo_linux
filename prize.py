from hdwallet import HDWallet
from hdwallet.symbols import BTC, ETH
import os
import time
import platform
from colorama import Fore, init
from pyfiglet import Figlet

init(autoreset=True)

def title():
    f = Figlet(font='standard')
    print(Fore.LIGHTCYAN_EX + f.renderText("Cryptonix") + Fore.RESET)

def get_clear():
    if 'win' in platform.platform() or 'Windows' in platform.platform():
        os.system('cls')
    elif 'linux' in platform.platform() or 'Linux' in platform.platform():
        os.system('clear')
    elif 'darwin' in platform.platform():
        os.system('clear')
    elif 'mac' in platform.platform() or 'Mac' in platform.platform():
        os.system('clear')
    else:
        raise ValueError('Not Supported Platform: "%s"' % platform.platform())

def load_checked_values(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            checked_values = {line.strip() for line in file}
    else:
        checked_values = set()
    return checked_values

def save_checked_value(file_path, value):
    with open(file_path, 'a') as file:
        file.write(f"{value}\n")

def load_target_addresses(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            target_addresses = {line.strip() for line in file}
    else:
        target_addresses = set()
    return target_addresses

def main():
    get_clear()
    print(Fore.GREEN, "Starting...", Fore.RESET)
    time.sleep(2)

    z = 1
    start_value = 0x3555555556aaaaaab
    end_value = 0x20000000000000000
    checked_file = 'check.txt'
    addresses_file = 'addresses.txt'

    checked_values = load_checked_values(checked_file)
    target_addresses = load_target_addresses(addresses_file)

    current_value = start_value

    while current_value >= end_value:
        private_key = f"{current_value:064x}"
        if private_key in checked_values:
            current_value -= 1
            continue

        try:
            print(f"Current value (dec): {current_value}, Private key: {private_key}")

            hd_btc: HDWallet = HDWallet(symbol=BTC)
            hd_eth: HDWallet = HDWallet(symbol=ETH)
            hd_btc.from_private_key(private_key)
            hd_eth.from_private_key(private_key)

            eth_addr = hd_eth.p2pkh_address()
            btc_addr1 = hd_btc.p2pkh_address()
            btc_addr2 = hd_btc.p2wpkh_address()
            btc_addr3 = hd_btc.p2wpkh_in_p2sh_address()
            btc_addr4 = hd_btc.p2wsh_in_p2sh_address()
            btc_addr5 = hd_btc.p2sh_address()

            if (btc_addr1 in target_addresses or btc_addr2 in target_addresses or
                btc_addr3 in target_addresses or btc_addr4 in target_addresses or
                btc_addr5 in target_addresses or eth_addr in target_addresses):
                print(Fore.GREEN + f"Found target address!\nCurrent value (dec): {current_value}, Private key: {private_key}" + Fore.RESET)
            
            save_checked_value(checked_file, private_key)
            checked_values.add(private_key)

            current_value -= 1
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Restarting...")
            time.sleep(5)
            main()

if __name__ == "__main__":
    main()
