import json
import re
import requests
from pyquery import PyQuery as pq

def get(url):
  resp = requests.get('http://icd9cm.chrisendres.com/index.php' + url)
  html = resp.content
  dom = pq(html)
  return dom

stack = [('?action=procslist', 'ICD-9-Proc', 'ICD9 Procedure Codes', 0)]

codes = {
    'ICD-9-Proc': {
      'desc': 'ICD9 Procedure Codes',
      'children': []
    }
}

visited = set()

while stack:
  url, parent, desc, depth = stack.pop()
  dom = get(url)
  print(' '*depth, parent, desc)

  visited.add(url)

  for link in dom.find('table[align="left"][width="100%"] a'):
    href = link.attrib['href'].replace('/index.php', '')
    text = link.text_content().strip()

    if href in visited: continue
    if text in visited: continue
    visited.add(text)

    if url == '?action=procslist':
      code = re.search("\((\d+\-?\d*)\)", text).group(1)
      desc = re.search(
          "[\dA-Z]+\.\s*(.*)\s\(\d+\-?\d*\)",
          text.replace(' , ', ', ')).group(1)
    else:
      match = re.search("(\d+\.?\-?\d*)\s(.*)$", text)
      if not match:
        import pdb; pdb.set_trace()
      code = match.group(1)
      desc = match.group(2)

    #print('adding {}, {}, children at {}'.format(code, desc, href))
    codes[code] = { 'desc': desc, 'children': [] }
    codes[parent]['children'].append(code)
    stack.append((href, code, desc, depth+1))

  for div in dom.find('table[align="left"][width="100%"] div.dlvl'):
    text = div.text_content().strip()
    if text in visited: continue
    visited.add(text)
    match = re.search("(\d+\.?\-?\d*)\s(.*)$", text)
    if not match:
      print('WARNING: no match for {}'.format(text))
      continue
    code = match.group(1)
    desc = match.group(2)

    print(' '*(depth+1), code, desc)
    codes[code] = { 'desc': desc, 'children': [] }
    codes[parent]['children'].append(code)

with open('./icd9-proc-codes.json','w') as f:
  f.write(json.dumps(codes, indent=4))
