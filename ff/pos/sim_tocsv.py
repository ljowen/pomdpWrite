fin = open('ff.simout', 'r');
fout = open('ff.simout.csv', 'w');
fout.write("SimNum, Pc_x, Pc_y, Pr, GPS");
simnum = 0;
for line in fin:
    if 'begin' in line: # if new sim
        simnum += 1;
    if 'X' in line: # IF state line
        # Pc_xy     
        l2 = repr(simnum) + ','
        subline = line[line.find('Pc') : line.find('Pc') + 5];
        l2 += subline.replace('Pc','').replace('_',',');
        
        # Pr
        subline2 = line[line.find('Pr')+2 : line.find('Pr') + 3];
        l2 += ',' + subline2;
        
        #GPS
        if 'OFF' in line:
            l2 += ',' + repr(0);
        if 'ON' in line:
            l2 += ',' + repr(1);
        if 'LOCK' in line:
            l2 += ',' + repr(2);
        fout.write(l2 + '\n');
        print l2;
    else:
        continue;
fout.close();
fin.close();
quit();
