from bs4 import BeautifulSoup
import sys
import re
import os.path as op

html = sys.argv[1]

with open(html, 'r') as f:
    contents = f.read()

pattern = re.compile(r'NEET_2024_Result/\d+\.pdf$')
soup = BeautifulSoup(contents, 'html.parser')

links = []
for link in soup.find_all('a', href=pattern):
    links.append(link)

with open(op.basename(html + '.links.txt'), 'w') as fout:
    fout.write('\n'.join([link['href'] for link in links]))
