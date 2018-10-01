import json

with open('./icd9-cm-codes.json','r') as f:
  codes = json.load(f)

codes2 = {}

stack = [('ICD-9-CM', None)]

while stack:
  code, parent = stack.pop()

  codes2[code] = {
      'desc': codes[code]['desc'],
      'parent': parent,
      'children': codes[code]['children']
  }

  for child in codes[code]['children']:
    stack.append((child, code))

with open('./icd9-cm-codes.json','w') as f:
  f.write(json.dumps(codes2, indent=4))
