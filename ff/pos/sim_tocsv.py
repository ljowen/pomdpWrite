fin = open('10simout', 'r');
fout = open('10simout.csv', 'w');
for line in fin:
    if 'Pc' in line:
        subline = line[line.find('Pc') : line.find('Pc') + 5];
        l2 = subline.replace('Pc','').replace('_',',');
        fout.write(l2 + '\n');
        print subline;
    else:
        continue;
fout.close();
fin.close();
quit();
