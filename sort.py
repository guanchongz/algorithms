def qiucksort(obj,start,end):
    if(end-start<1):
        return
    t=obj[start]
    i=start+1
    j=end
    while 1:
        while obj[i]<t and i<end:
            i+=1
        while obj[j]>t:
            j-=1
        if j<=i:
            break
        x = obj[i]
        obj[i] = obj[j]
        obj[j] = x
        i+=1
        j-=1
    x = obj[start]
    obj[start] = obj[j]
    obj[j] = x
    print (i,j)
    qiucksort(obj,start,j-1)
    qiucksort(obj,j+1,end)
