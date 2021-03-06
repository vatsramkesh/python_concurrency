import time
import requests
import multiprocessing

session = None


def set_global_session():
    global session
    if not session:
        session = requests.Session()


def download_site(url):
    with session.get(url) as response:
        process_name = multiprocessing.current_process().name
        print(f"{process_name}:Read {len(response.content)} from {url}")


def download_all_sites(urls):
    with multiprocessing.Pool(initializer=set_global_session) as pool:
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