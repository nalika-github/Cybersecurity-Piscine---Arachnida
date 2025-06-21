import argparse
import sys
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_valid_image(filename):
    allowed_ext = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    return any(filename.lower().endswith(ext) for ext in allowed_ext)

def spider(depth, max_depth, visited, url, output_dir):
    print(f'depth = {depth}')
    print(f'max_depth = {max_depth}')
    if depth > max_depth or url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url, timeout = 5)
        if response.status_code != 200:
            print(f"Failed to load {url} [{response.status_code}]")
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #download image
        images = soup.find_all('img')
        for img in images:
            img_url = img.get('src')
            full_url = urljoin(url, img_url)
            dowonload_images(full_url, output_dir)

        # find and acess linked
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href:
                next_url = urljoin(url, href)
                spider(depth + 1, max_depth, visited, next_url, output_dir)
    except Exception as e:
        print(f"⚠️ Error crawling {url}: {e}")
 
def dowonload_images(img_url, output_dir):

    try:
        response = requests.get(img_url, timeout = 5)
        if response.status_code == 200:
            parsed_url = urlparse(img_url)
            filename = os.path.basename(parsed_url.path)
            if not filename or not is_valid_image(filename):
                return
            save_path = os.path.join(output_dir, filename)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f'✅ downloaded: {filename}')
        else:
            print(f'❌ unable to download: {filename}')
    except Exception as e:
        print(f'⚠️ Error {img_url}: {e}')
        
# test url: https://en.wikipedia.org/wiki/Example.com
def main():
    parser = argparse.ArgumentParser(prog='Spider', description = '''   
    The spider program allow you to extract all the images from a website, recursively, by
    providing a url as a parameter 
                                    ''')
    parser.add_argument('-r', action = 'store_true', help = 'Recursively downloads images from the given URL.')
    parser.add_argument('-l', type = int, default = 5, help = 'Maximum depth level of recursive download (requires -r). Default is 5.')
    parser.add_argument('-p', type = str, default = "./data/", help = 'Path to save downloaded files. Default is ./data/')
    parser.add_argument('URL', type = str, help = 'The starting URL')

    args = parser.parse_args()
    os.makedirs(args.p, exist_ok = True)
    visited = set()

    if args.r:
        spider(0, args.l, visited, args.URL, args.p)
    else:
        response = requests.get(args.URL)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.find_all('img')
            for img in images:
                img_url = img.get('src')
                full_url = urljoin(args.URL, img_url)
                dowonload_images(full_url, args.p)
        else:
            print("Webpage failed to load", response.status_code)
            sys.exit(-2)
    
if __name__ == "__main__":
    main()