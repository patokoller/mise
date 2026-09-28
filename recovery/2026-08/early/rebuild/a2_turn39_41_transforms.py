# Session f00a0b22: turn 39 sed (Danish folding) + turn 41 two patches (D-038 Anarki, D-039 Propaganda), verbatim logic.
p="build_a2_frame.py"; s=open(p,encoding="utf-8").read()
# turn 39: sed -i 's|def norm(s):|def norm(s):\n    s=s.replace("ø","o")...|'
s=s.replace('def norm(s):','def norm(s):\n    s=s.replace("ø","o").replace("Ø","O").replace("æ","ae").replace("å","aa")',1)
# turn 41 patch 1
old='out=[]\nfor name,addr_raw,tier,flag,note in rows:'
new='''out=[]
# D-038: Anarki is Masters. The Very Fine rendering is superseded and is not carried as a row.
rows=[x for x in rows if not (x[0]=="Anarki" and x[2]=="Very Fine")]
for name,addr_raw,tier,flag,note in rows:
    if name=="Propaganda - next door":
        name="Propaganda"; note=("D-039: recorded as one venue with Propaganda; 'next door' held as an alias. "
                                 "White Guide lists the sub-concept; Places returns a single establishment.")
    if name=="Anarki":
        note=("D-038: source rendered this venue ID at both Very Fine and Masters. Operator confirmed Masters current; "
              "the Very Fine rendering is superseded and not carried as a second row.")'''
assert old in s; s=s.replace(old,new)
s=s.replace('("A2 listing rows (Anarki appears twice)",f\'=COUNTA(A5:A{last})\'),\n   ("Unique venues",f\'=COUNTA(A5:A{last})-1\'),',
            '("A2 unique venues (one row per venue)",f\'=COUNTA(A5:A{last})\'),')
s=s.replace('ws["A2"]=("Route A2 only. F1 applied to RESOLVED ADDRESSES',
            'ws["A2"]=("Route A2 only. One row per venue. F1 applied to RESOLVED ADDRESSES')
# turn 41 patch 2: rename after resolution
old='''    if name=="Propaganda - next door":
        name="Propaganda"; note=("D-039: recorded as one venue with Propaganda; 'next door' held as an alias. "
                                 "White Guide lists the sub-concept; Places returns a single establishment.")
'''
assert old in s; s=s.replace(old,'')
old2='    out.append(dict(n=name,'
new2='''    if name=="Propaganda - next door":
        name="Propaganda"
        f0=("D-039: recorded as one venue with Propaganda; 'next door' held as an alias. "
            "White Guide lists the sub-concept; Places returns a single establishment.")
    out.append(dict(n=name,'''
assert old2 in s; s=s.replace(old2,new2)
open(p,"w",encoding="utf-8").write(s); print("transforms applied")
