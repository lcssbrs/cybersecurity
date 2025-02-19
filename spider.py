import argparse
import os
from bs4 import BeautifulSoup
import requests

default_path = "./data/"
default_error_depth = 0
default_depth = 5
default_recursive = False
data = None
all_links = []


extension = {".jpg", ".jpeg", ".gif", ".bmp", ".png"}

def get_parser():
    parse_element = argparse.ArgumentParser(description="Spider")
    parse_element.add_argument("url", help="URL to start spidering")
    parse_element.add_argument("-r", "--recursive", action="store_true", default=default_recursive, help="Recursive spidering")
    parse_element.add_argument("-l", "--depth", type=int, default=default_error_depth, help="Depth to spider")
    parse_element.add_argument("-p", "--path", default=default_path, help="Path directory")
    return parse_element

def complete_url(url):
    if url.startswith("http://") or url.startswith("https://"):
        return url
    elif url.startswith("www."):
        url = "http://" + url
        return url
    else:
        url = "http://www." + url
        return url

def check_url(link):
    link = complete_url(link)
    try:
        data = requests.get(link)
        return data
    except requests.exceptions.RequestException:
        print("URL not found")
        exit(1)

def set_variables():
    parser = get_parser()
    url = parser.parse_args().url
    path = parser.parse_args().path
    depth = parser.parse_args().depth
    recursive = parser.parse_args().recursive
    return url, path, depth, recursive

def download_image(url):
    try:
        image = requests.get(url)
        with open(os.path.basename(url), "wb") as file:
            file.write(image.content)
    except requests.exceptions.RequestException:
        print("Image not found")
        exit(1)

def fetch_data(soup):
    images = soup.find_all("img")
    for image in images:
        src = image.get("src")
        if src is not None:
            if src.endswith(tuple(extension)):
                print("Image found: ", src)
                download_image(src)

def check_link(link):
    if link in all_links:
        return True
    all_links.append(link)
    return False

def ft_recursive(soup, depth):
    fetch_data(soup)
    if depth == 0:
        return
    links = soup.find_all("a")
    i = 0
    while i < len(links) and depth > 0:
        link = links[i].get("href")
        if link is not None:
            if check_link(link):
                break
            if link.startswith("http"):
                print("depth: ", depth, "link: ", link)
                data = check_url(link)
                soup = BeautifulSoup(data.text, "html.parser")
                ft_recursive(soup, depth - 1)
        i += 1

if __name__ == "__main__":
    url, path, depth, recursive = set_variables()
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
