import json, sys, os
d = json.load(open(sys.argv[1]))
n = {e['name']: e for e in d['entries']}
for l in open('/tmp/vp25/final2.txt'):
    s, v = l.split()[:2]
    b = 'vb25-' + s.replace('_', '-', 1) + '-' + v
    if b + '.wav' in n and not os.path.exists(f'/mnt/user-data/outputs/vb25/all/{b}.mp3'):
        log = n.get(b + '.log')
        print(b)
