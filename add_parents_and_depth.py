import json

for root, fname in [
    ('CPT-4', './cpt-parent-codes.json'),
    ('ICD-9-Proc', './icd9-proc-codes.json'),
    ('ICD-9-CM', './icd9-cm-codes.json'),
  ]:

  with open(fname,'r') as f:
    codes = json.load(f)

  codes2 = {}
  stack = [(root, None, 0)]
  while stack:
    code, parent, depth = stack.pop()
    print(code,parent,depth)
    if depth > 10:
      raise
    if code in codes:
      codes2[code] = codes[code]
      codes2[code]['parent'] = parent
      codes2[code]['depth'] = depth
      children = [c for c in codes[code]['children'] if c != code]
      codes2[code]['children'] = children
      for child in children:
        if child == parent:
          import pdb
          pdb.set_trace()
        stack.append((child, code, depth+1))
    else:
      codes2[code] = {
          'parent': parent,
          'depth': depth,
          'children': [],
          'desc': ''
      }

  with open(fname, 'w') as f:
    f.write(json.dumps(codes2, indent=2))
