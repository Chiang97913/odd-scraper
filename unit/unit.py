import requests
import time
import urllib3
urllib3.disable_warnings()

def robust_request(url, method='get', header=None, delay=5, max_retries=50, **kwargs):

    header_default = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.4844.74 Safari/537.36"
    }
    if header:
        header_default.update(header)
    retries = 0
    while retries < max_retries:
        try:
            if method.lower() == 'get':
                response = requests.get(url, headers=header_default,verify=False, **kwargs)
            elif method.lower() == 'post':
                response = requests.post(url, headers=header_default,verify=False, **kwargs)

            else:
                raise ValueError("Unsupported method: " + method)
            if response.status_code == 200:
                return response
            if response.status_code == 404:
                print(f"404页面！{url} ")
                return 404
            else:
                print(f"{url} Attempt {retries + 1} failed with status code {response.status_code}. Retrying...")
                retries += 1
                time.sleep(delay)

        except requests.RequestException as e:
            print(f"{url} An error occurred: {e}. Retrying...")
            retries += 1
            time.sleep(delay)

    raise Exception(f"Request failed after {max_retries} attempts.")


