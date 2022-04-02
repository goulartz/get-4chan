import requests
import argparse
import os
from progress.bar import Bar
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(add_help=False)

parser.add_argument('--help', default=argparse.SUPPRESS, help='Show this help message', action='help')
parser.add_argument('--thread', type=str, help="Specify the thread to download", metavar='\b', required=True)
parser.add_argument('--path', type=str, help="Create OR specify the destination directory", metavar='\b', required=True)
args = parser.parse_args()

## Caso não tenha https no começo do parâmetro thread
if not args.thread.startswith("https://"):
	if args.thread.startswith("http://"):
		arg.thread.replace("http://", "https://")
	else:
		args.thread = "https://" + args.thread

if not args.path.endswith("/"):
	args.path = args.path + "/"

#Criar pasta de destino
try:
    os.mkdir(args.path)
except OSError:
    pass

## Download das imagens da thread
thread = requests.get(args.thread)
bs = BeautifulSoup(thread.text, 'html.parser')
images = bs.find_all('a', {'class': 'fileThumb', 'href': True})
bar = Bar('Download', max = len(images), suffix='%(percent)d%%')
for image in images:
    bar.next()
    with requests.get("https:" + str(image['href'])) as r:
        split = str(image['href']).split('/')
        with open(args.path + split[4], "wb") as binary_img:
            binary_img.write(r.content)
            binary_img.close()         
bar.finish()      
