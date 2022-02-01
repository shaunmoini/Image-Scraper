import os
import sys
import signal
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def main():
  url = input('Enter URL: ')
  directory = input('Enter folder name: ')
  print()
  download_images(url, directory)
  print()
  main()

def download_images(url, directory):
  # requesting and parsing html
  try:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
  except Exception as e:
    print(e)
    return
  
  soup = BeautifulSoup(response.text, 'html.parser')
  imgs = soup.find_all('img')
  img_urls = extract_urls(imgs)
  working_directory = os.getcwd()

  # checking if list is empty
  if(not img_urls):
    print('No accessible images found.')
    return

  # creating directories for downloaded images
  try:
    if(os.path.isdir(os.path.join(os.getcwd(), 'downloads'))):
      os.mkdir(os.path.join(os.getcwd(), 'downloads', directory))
      os.chdir(os.path.join(os.getcwd(), 'downloads', directory))
    else:
      os.mkdir(os.path.join(os.getcwd(), 'downloads'))
      os.mkdir(os.path.join(os.getcwd(), 'downloads', directory))
      os.chdir(os.path.join(os.getcwd(), 'downloads', directory))
  except FileExistsError:
    print('Folder already exists.')
    return
  except Exception as e:
    print(e)
    return

  # iterating through imgs list and writing image data to files
  counter = 1
  for url in img_urls:
    try:
      img_response = requests.get(url)
      # filtering out image files smaller than 1000 bytes
      if(len(img_response.content) < 1000):
        continue
    except Exception as e:
      print(e)
      continue

    with open(str(counter) + '.jpg', 'wb') as f:
      f.write(img_response.content)
      print('Downloading image', counter)
    
    counter += 1
  
  os.chdir(working_directory)
  print('\nDone!')

def extract_urls(imgs):
  result = []
  for img in imgs:
    try:
      img_url = img['src']
      if('http' not in img_url):
        img_url = 'http:' + img_url
      if(is_valid_url(img_url)):
        result.append(img_url)
    except:
      continue
    
  return result

def is_valid_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

def exit_gracefully (signal, frame):
  print ('\n\nGoodbye!')
  sys.exit(0)

print('Press "CTRL+C" to quit anytime.\n')
signal.signal(signal.SIGINT, exit_gracefully)
main()