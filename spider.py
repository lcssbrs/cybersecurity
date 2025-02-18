import os
import sys
from os import mkdir
from sys import argv
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup

#function to complete the URL if it is incomplete
def completeUrl(url):
    if url.startswith('www.'):
        url = 'http://' + url
    elif url.startswith('http://') or url.startswith('https://'):
        pass
    else:
        url = 'http://www.' + url
    return url

#function to check if the argument is a valid URL by pinging the URL
def isUrl(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return True
    except requests.RequestException:
        return False

#function to parse arguments
def parse_args(argv):
    if len(argv) == 1:
        print('Usage: python spider.py <url>')
        exit(1)
    if len(argv) > 2:
        print('Too many arguments')
        exit(1)
    if not isUrl(argv[1]):
        print('Invalid URL')
        exit(1)
    return argv[1]

#function to get the html content of a page
def getHtml(url):
    response = requests.get(url)
    return response.text

#function to get the image links from the html content recursively
def parseImages(html):
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('img')
    folder = 'images_' + sys.argv[1].split('//')[1]
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass
    try:
        os.chdir(folder)
    except FileNotFoundError:
        pass
    for image in images:
        image = image.get('src')
        if image.endswith('.jpg') or image.endswith('.png') or image.endswith('.jpeg') or image.endswith('.gif') or image.endswith('.bmp'):
            downloadImages(image)


#function to download the images
def downloadImages(image):
    try:
        urlretrieve(image, os.path.basename(image))
    except Exception as e:
        print(e)

#function to save the images to a folder

#function to run the spider
if __name__ == '__main__':
    if len(argv) == 1:
        argv.append('https://www.google.com')
    argv[1] = completeUrl(argv[1])
    if isUrl(argv[1]):
        print("URL is valid")
    else:
        print("URL is invalid")
        exit(1)
    html = getHtml(argv[1])
    parseImages(html)
