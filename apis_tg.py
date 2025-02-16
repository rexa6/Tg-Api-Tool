import requests
from bs4 import BeautifulSoup
from colorama import Fore, init
from time import sleep

init()

def print_banner():
    print(f"""{Fore.CYAN}
   ____     _____     _____              ________    _____   _____      
  (    )   (  __ \   (_   _)            (___  ___)  / ___/  (_   _)     
  / /\ \    ) )_) )    | |    ________      ) )    ( (__      | |       
 ( (__) )  (  ___/     | |   (________)    ( (      ) __)     | |       
  )    (    ) )        | |                  ) )    ( (        | |   __  
 /  /\  \  ( (        _| |__               ( (      \ \___  __| |___) ) 
/__(  )__\ /__\      /_____(               /__\      \____\ \________/  
                                                                        
    {Fore.YELLOW}Tool to get api hash and api id of telegram account 
    {Fore.LIGHTGREEN_EX}Git & Telegram : @r1exa6\n
""")

def get_api_data(phone_number):
    with requests.Session() as req:
        login0 = req.post('https://my.telegram.org/auth/send_password', data={'phone': phone_number})
        
        if 'Sorry, too many tries. Please try again later.' in login0.text:
            print(f'{Fore.RED}Your account has been banned!\nPlease try again in 8 hours.')
            exit()

        login_data = login0.json()
        random_hash = login_data['random_hash']

        code = input(f'{Fore.RED}[{Fore.GREEN}+{Fore.RED}] {Fore.GREEN}Send the code sent in the Telegram account: {Fore.RED}')

        login_data = {
            'phone': phone_number,
            'random_hash': random_hash,
            'password': code
        }
        
        login = req.post('https://my.telegram.org/auth/login', data=login_data)
        return req

def extract_api_data(req):
    try:
        apps_page = req.get('https://my.telegram.org/apps')
        soup = BeautifulSoup(apps_page.text, 'html.parser')

        api_id = soup.find('label', string='App api_id:').find_next_sibling('div').select_one('span').get_text()
        api_hash = soup.find('label', string='App api_hash:').find_next_sibling('div').select_one('span').get_text()
        key = soup.find('label', string='Public keys:').find_next_sibling('div').select_one('code').get_text()
        Pc = soup.find('label', string='Production configuration:').find_next_sibling('div').select_one('strong').get_text()
       
        sleep(3)

        print(f"""{Fore.GREEN}
    __    ____  ____ 
    /__\  (  _ \(_  _)
    /(__)\  )___/ _)(_ 
    (__)(__)(__)  (____)

    {Fore.CYAN}APIs successfully received:

        {Fore.RED}[{Fore.GREEN}+{Fore.RED}] {Fore.GREEN}Api ID: {Fore.YELLOW}{api_id}
        {Fore.RED}[{Fore.GREEN}+{Fore.RED}] {Fore.GREEN}Api HASH: {Fore.YELLOW}{api_hash}
        
        {Fore.RED}[{Fore.GREEN}~{Fore.RED}] {Fore.GREEN}Public Key: {Fore.YELLOW}{key}
        {Fore.RED}[{Fore.GREEN}~{Fore.RED}] {Fore.GREEN}Production configuration: {Fore.YELLOW}{Pc}
        
    """)
    except Exception as e:
        print(f'{Fore.RED}An error occurred while retrieving API data: {str(e)}')

def main():
    print_banner()

    phone = input(f"{Fore.RED}[{Fore.GREEN}+{Fore.RED}] {Fore.GREEN}Enter your number along with the country code [Ex : +98XXXXXX]: {Fore.RED}")

    req = get_api_data(phone)
    
    extract_api_data(req)

if __name__ == '__main__':
    main()
