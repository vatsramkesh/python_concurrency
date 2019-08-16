import concurrent.futures
import requests
import threading
import time

local_thread = threading.local()


def get_session():
    if not hasattr(local_thread, "session"):
        local_thread.session = requests.Session()
    return local_thread.session


def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites(urls):
    with concurrent.futures.ThreadPoolExecutor() as pool:
        pool.map(download_site, urls)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 20
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")
