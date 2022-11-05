effect = []
mechanism = []
intt = []
advise = []
with open('svo.check') as f:
    for line in f:
        if str(line).startswith('P('):
            a = str(line).split("=")
            num = str(a[1]).split("/")
            if len(num) > 1:
                if not str(a[0]).startswith("P(null"):
                    if int(num[1]) >=2 and int(num[1]) <= 20:
                        if(float(a[2]) >= 0.6):
                            if(str(a[0]).startswith("P(effect")):
                                effect.append(str(a[0]).split('|')[1].split(")")[0])
                            elif (str(a[0]).startswith("P(mechanism")):
                                mechanism.append(str(a[0]).split('|')[1].split(")")[0])
                            elif (str(a[0]).startswith("P(int")):
                                intt.append(str(a[0]).split('|')[1].split(")")[0])
                            elif (str(a[0]).startswith("P(advise")):
                                advise.append(str(a[0]).split('|')[1].split(")")[0])  
                    if int(num[1]) >20:
                        if float(a[2]) >= 0.5:
                            if(str(a[0]).startswith("P(effect")):
                                effect.append(str(a[0]).split('|')[1].split(")")[0])
                            elif (str(a[0]).startswith("P(mechanism")):
                                mechanism.append(str(a[0]).split('|')[1].split(")")[0])
                            elif (str(a[0]).startswith("P(int")):
                                intt.append(str(a[0]).split('|')[1].split(")")[0])
                            elif (str(a[0]).startswith("P(advise")):
                                advise.append(str(a[0]).split('|')[1].split(")")[0])  



print(f"\n\nEFFECT LIST: {effect}")

print(f"\n\nMECHANISM LIST: {mechanism}")

print(f"\n\nADVISE LIST: {advise}")

print(f"\n\nINT LIST: {intt}")



#file1.close()
        
