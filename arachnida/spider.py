import argparse
import os
import yarl
import uuid

from bs4 import BeautifulSoup
import requests

default_path = "./data/"
default_error_depth = 0
default_depth = 5
default_recursive = False
data = None
all_links = set()


extension = {".jpg", ".jpeg", ".gif", ".bmp", ".png"}

def get_parser():
    parse_element = argparse.ArgumentParser(description="Spider")
    parse_element.add_argument("url", help="URL to start spidering")
    parse_element.add_argument("-r", "--recursive", action="store_true", default=default_recursive, help="Recursive spidering")
    parse_element.add_argument("-l", "--depth", type=int, default=default_error_depth, help="Depth to spider")
    parse_element.add_argument("-p", "--path", default=default_path, help="Path directory")
    return parse_element

def complete_url(url):
    if url.endswith("/") is False:
        url += "/"
    if url.startswith("http") or url.startswith("https"):
        return url
    return "http://" + url


def check_url(link):
    link = complete_url(link)
    try:
        data = requests.get(link)
        return data
    except requests.exceptions.RequestException:
        print("URL not found")
        return None
def set_variables():
    parser = get_parser()
    url = parser.parse_args().url
    path = parser.parse_args().path
    depth = parser.parse_args().depth
    recursive = parser.parse_args().recursive
    return url, path, depth, recursive

def download_image(url):
    try:
        data = requests.get(url)
        link = url.split("/")[-1]
        with open(link + str(uuid.uuid4()) + ".jpg", "wb") as file:
            file.write(data.content)
    except requests.exceptions.RequestException:
        print("Image not found")


def fetch_data(soup):
    images = soup.find_all("img")
    for image in images:
        src = image.get("src")
        if src is not None:
            if src.endswith(tuple(extension)):
                download_image(src)


def normalize_url(link):
    url = yarl.URL(link)
    scheme = "https"
    if url.host:
        host = url.host.lstrip("www.")
        path = url.path.rstrip("/")
        return f"{scheme}://{host}{path}"
    return

def check_link(link):
    normalized_link = normalize_url(link)
    if normalized_link in all_links:
        return True
    all_links.add(normalized_link)
    return False

def ft_recursive(soup, depth):
    if depth == 0:
        exit(0)
    print("depth: ", depth)
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href is not None:
            if not check_link(href):
                data = check_url(href)
                if data:
                    soup = BeautifulSoup(data.text, "html.parser")
                    fetch_data(soup)
                    ft_recursive(soup, depth - 1)

if __name__ == "__main__":
    url, path, depth, recursive = set_variables()
    all_links.add(normalize_url(complete_url(url)))
    print("all_links: ", all_links)
    if not recursive and depth != default_error_depth:
        print("The depth option is only available with the recursive option")
        exit(1)
    if depth < default_error_depth:
        print("The depth option must be a positive integer")
        exit(1)
    depth = default_depth if depth == default_error_depth else depth
    data = check_url(url)
    soup = BeautifulSoup(data.text, "html.parser")
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    os.chdir(path)
    if recursive:
        ft_recursive(soup, depth)
    else:
        fetch_data(soup)
