while True:
    try:
        m=input().strip().split()
        key=["reset","reset board","board add","board delete","reboot backplane","backplane abort"]
        value=["reset what","board fault","where to add","no board at all","impossible","install first"]
        #key[2][:3] 'boa'
        #不建字典，是因为字典可能无序（3版又改动了），不方便确认是否唯一
        if len(m)<1 or len(m)>2:
            print("unknown command")
        elif len(m)==1:
            if m[0]==key[0][:len(m[0])]:
                print(value[0])
            else:
                print("unknown command")
        else:
            index=[]
            for i in range(1,len(key)):
                a=key[i].split()
                #print(a[0][:3])
                if m[0]==a[0][:len(m[0])] and m[1]==a[1][:len(m[1])]:
                    index.append(i)
            if len(index)!=1:
                print("unknown command")
            else:
                print(value[index[0]])
    except:
        break