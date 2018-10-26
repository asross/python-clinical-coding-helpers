import json
import re
import requests
from pyquery import PyQuery as pq

def get(url):
  resp = requests.get('https://www.supercoder.com' + url)
  html = resp.content
  dom = pq(html)
  return dom

stack = [('/cpt-codes-range', 'CPT-4', 'CPT-4 Procedure Codes', 0)]

codes = {
    'CPT-4': {
      'desc': 'CPT-4 Procedure Codes',
      'children': []
    }
}

while stack:
  url, parent, desc, depth = stack.pop()
  dom = get(url)
  print(' '*depth, parent, desc)

  for div in dom.find('.padtop-white'):
    links = div.cssselect('a')
    if len(links) == 2:
      a1, a2 = links
      code = a1.text.replace(' ', '')
      desc = a2.text.strip()
      codes[code] = {
          'desc': desc,
          'children': []
      }
      codes[parent]['children'].append(code)
      stack.append((a1.attrib['href'], code, desc, depth+1))
    elif len(links) == 1:
      minc, maxc = [int(c) for c in parent.split('-')]
      for code in range(minc, maxc+1):
        print(' '*(depth+1), code)
        codes[parent]['children'].append(str(code))
      break
    else:
      import pdb; pdb.set_trace()
      pass

with open('./cpt-parent-codes.json','w') as f:
  f.write(json.dumps(codes, indent=4))
