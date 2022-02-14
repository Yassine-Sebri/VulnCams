import shodan
import time


def shodan_search():
    SHODAN_API_KEY = input("Provide a Shodan API key: ")

    shodan_api = shodan.Shodan(SHODAN_API_KEY)
    result = shodan_api.count('country:"TN" port:"37777"')["total"]
    print(f'[+] Possible Number of Public Dahua Devices: {result}')
    pages = result // 100
    Dahua_IPs = ()
    time.sleep(3)
    print('[+] Retrieving IP addresses. This might take some time.')
    for page in range(pages):
        time.sleep(3)
        results = shodan_api.search('country:"TN" port:"37777"', page=page+1)
        for result in results['matches']:
            if result['ip_str'] != '':
                Dahua_IPs = Dahua_IPs + (result['ip_str'] + '\n',)
    print(f'[+] Number of IPs retrieved: {len(Dahua_IPs)}')
    print('[+] Saving found IP addresses to "Shodan_IPs.txt"')
    with open("Shodan_IPs.txt", 'w+') as file:
        file.writelines(Dahua_IPs)


def masscan():
    with open('TN_IPs.txt', 'r') as file:
        TN_IPs = file.readlines()


def main():
    shodan_search()


if __name__ == '__main__':
    main()
