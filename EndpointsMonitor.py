import requests
import yaml
import time
from collections import defaultdict
from urllib.parse import urlparse

def load_endpoints(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def check_endpoint(endpoint):
    method = endpoint.get('method', 'GET')
    url = endpoint['url']
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)
    response = requests.request(method, url, headers=headers, data=body, timeout=0.5)
    return response.status_code // 100 == 2

def monitor_endpoints(file_path):
    endpoints = load_endpoints(file_path)
    domain_availability = defaultdict(lambda: [0, 0])  

    while True:
        for endpoint in endpoints:
            domain = urlparse(endpoint['url']).netloc
            try:
                if check_endpoint(endpoint):
                    domain_availability[domain][0] += 1
            except requests.exceptions.RequestException:
                pass
            finally:
                domain_availability[domain][1] += 1

        for domain, (successful_checks, total_checks) in domain_availability.items():
            availability = (successful_checks / total_checks) * 100
            print(f'{domain} has {round(availability)}% availability percentage')

        time.sleep(15)

monitor_endpoints('endpoints.yaml')