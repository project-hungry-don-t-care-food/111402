infile=open('Restaurant data.csv','r',encoding='utf-8')
outfile=open('out2.csv','w',encoding='utf-8')

data=infile.readlines()

outdate=[]
for d in data:
    d=d.strip().split(',')
    name=str(d[1])
    link=str(d[4])
    outdate.append(f'{name},{link}\n')

outdate[-1]=outdate[-1].strip()
print(outdate)
outfile.writelines(outdate)

infile.close()
outfile.close()