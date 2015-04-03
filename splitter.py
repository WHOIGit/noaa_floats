import re

for line in open('data/floats_dirfl.dat'):
    line = line.rstrip()
    line = re.sub(r'^\s+','',line)
    def type_coerce(val):
        try:
            return int(val)
        except:
            pass
        try:
            return float(val)
        except:
            pass
        return val
    cols = map(type_coerce,re.split(r'\b(?:\s*\t+\s*|\s\s)(?=[-0-9a-zA-Z])',line))
    print len(cols), cols
