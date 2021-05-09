f = open(".txt", 'r', encoding='UTF8')
text = ''
a = []
for c in range (3000):
        row = f.readline()
        if not row: break
        if row == '[]':
                continue
        text += row
        text = text.replace('[','')
        text=text.replace('\'','')
        text = text.replace(']','')
        text = text.replace('\n',',')
        t=[i for i in text.split(',')]
        for j in t:
                a.append(j)
        while '' in a:
                a.remove('')
        text = ''
f.close()

a_cnt = dict()

for i in list(set(a)):
        a_cnt[i] = a.count(i)
b = a_cnt

b_val_reverse = sorted(b.items(),
                       reverse=True,
                       key=lambda item:item[1])

for items in b_val_reverse:
        print(items[0],':',items[1])
