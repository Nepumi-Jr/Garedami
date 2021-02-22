from Garedami.Src import Config
from Garedami.Src.Annouce import *

def CheckIsDanger(srcStr:str,words:list):

    for word in words:
        if srcStr.find(word) != -1:
            printError(f"Found Danger word!{word}")
            return word
    
    return False

def RedixSort(con):
    n = len(con)

    crt = [0]*n
    pos = [0]*n
    new_con = [(0,0,0)]*n

    for e in con:
        crt[e[0]] += 1

    pos[0] = 0;
    for i in range(1,n):
        pos[i] = pos[i-1] + crt[i-1];

    for e in con:
        new_con[pos[e[0]]] = e;
        pos[e[0]]+=1

    return new_con.copy()

def CheckBySuffixArray(srcStr:str,words:list):
    srcStr += chr(0)
    P = [0]*(len(srcStr)+10)
    C = [0]*(len(srcStr)+10)
    n = len(srcStr)


    #Building Suffix array
    F = [(chr(0),0)] * n
    for i in range(n):
        F[i] = (srcStr[i],i)
    
    F = sorted(F)

    P[0] = F[0][1]
    C[P[0]] = 0
    now_c = 0
    for i in range(1,n):
        if(F[i][0] != F[i-1][0]):
            now_c+=1
        P[i] = F[i][1]
        C[P[i]] = now_c
    
    F.clear()

    

    p = 1

    while p < n:

        Con = [(0,0,0)]*n
        for i in range(n):
            Con[i] = (C[(P[i]-p+n)%n],C[P[i]],(P[i]-p+n)%n)

        Con = RedixSort(Con)

        P[0] = Con[0][2]
        C[P[0]] = 0
        now_c = 0
        for i in range(1,n):
            if((Con[i][0],Con[i][1]) != (Con[i-1][0],Con[i-1][1])) : 
                now_c+=1
            P[i] = Con[i][2]
            C[P[i]] = now_c

        p<<=1
    
    
    
    for word in words:
        nq = len(word)

        noi = 0
        mak = n-1

        while(noi<=mak):
            mid = noi+(mak-noi)//2
            res = 0
            for i in range(nq):
                if(word[i]!=srcStr[(P[mid]+i)%n]):
                    if(word[i]<srcStr[(P[mid]+i)%n]):
                        res = -1
                        break
                    else:
                        res = 1
                        break
            
            if(res == 0):
                return word
            elif(res == -1):
                mak = mid-1
            else:
                noi = mid+1

    return False


def IsDanger(srcStr:str, srcLang:str):

    danger = Config.getDangerWord()
    res = CheckBySuffixArray(srcStr,danger)
    if res != False:
        printError(f"Found Danger word!{res}")

    dangerLang = Config.getDangerWordByLang(srcLang)
    res = CheckBySuffixArray(srcStr,dangerLang)
    if res != False:
        printError(f"Found Danger word!{res}")
    
    return res


if __name__ == "__main__":
    print(CheckBySuffixArray("Test",["meow"]))
    print(CheckBySuffixArray("Test",["Test"]))
    print(CheckBySuffixArray("Test nya",["Test"]))
    print(CheckBySuffixArray("#include<bits/stdc++.h>\nint main(){}",["int main()"]))
    print(CheckBySuffixArray("if __name__ == \"__main__\": ",["int main()"]))





