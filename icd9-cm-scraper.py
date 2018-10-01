import json
import re
import requests
from pyquery import PyQuery as pq
from urlparse import urlparse

codes = {
  'ICD-9-CM': {
    'desc': '2015 ICD-9-CM Diagnosis Codes',
    'parent': None,
    'children': []
  }
}

stack = [('/2015/Volume1/default.htm', 'ICD-9-CM')]

def get(url):
  resp = requests.get('http://www.icd9data.com' + url)
  html = resp.content
  dom = pq(html)
  return dom

while stack:
  url, parent = stack.pop()
  dom = get(url)

  nodes = dom.find('.definitionList li')
  leaves = dom.find('.codeHierarchyUL li')

  if nodes:
    for li in nodes:
      link = li.find('a')
      code = link.text
      desc = re.sub("\s*"+code+"\s*", "", li.text_content()).strip()
      codes[parent]['children'].append(code)
      codes[code] = {
          'desc': desc,
          'parent': parent,
          'children': []
      }
      print(code, codes[code])
      stack.append((link.attrib['href'], code))

  if leaves:
    parents = []
    for li in leaves:
      code = li.find_class('identifier')[0].text
      desc = li.find_class('threeDigitCodeListDescription')[0].text
      while parents and not code.startswith(parents[-1]):
        parents.pop()
      local_parent = parents[-1] if parents else parent
      codes[local_parent]['children'].append(code)
      codes[code] = {
          'desc': desc,
          'parent': local_parent,
          'children': []
      }
      print(code, codes[code])
      parents.append(code)

with file('./icd9-cm-codes.json','w') as f:
  f.write(json.dumps(codes, indent=4))
