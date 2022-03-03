def rpn(s):
    lex=parse(s)
    s2=[]
    r=[]
    oper=["+","-","*","/","(",")"]
    for a in lex:
        if a=="(":
            s2=[a]+s2
        elif a in oper:
            if s2==[]:
                s2=[a]
            elif a==")":
                while(True):
                    q=s2[0]
                    s2=s2[1:]
                    if q=="(":
                        break
                    r+=[q]
            elif prty(s2[0]) < prty(a):
                s2=[a]+s2
            else:
                while(True):
                    if s2==[]:
                        break
                    q=s2[0]
                    r+=[q]
                    s2=s2[1:]
                    if prty(q)==prty(a):
                        break
                s2=[a]+s2
        else:
            r+=[a]
    while(s2 != []):
        q=s2[0]
        r+=[q]
        s2=s2[1:]
    return r
 
def prty(o):
    if o=="+" or o=="-":
        return 1
    elif o=="*" or o=="/":
        return 2
    elif o=="(":
        return 0
 
def parse(s):
    delims=["+","-","*","/","(",")"]
    lex=[]
    tmp=""
    for a in s:
        if a != " ":
            if a in delims:
                if tmp != "":
                    lex+=[tmp]
                lex+=[a]
                tmp=""
            else:
                tmp+=a
    if tmp != "":
        lex+=[tmp]
    return lex

def fac(n):
    if n == 0:
        return 1
    return fac(n - 1) * n

def calculate(text): 
    polskiu = []

    # text = "Сколько будет 76+5*(3-6)"

    l = list(text)
    a = []
    b = []
    c = []
    slv = 0
    cc = ''

    for i in range(len(l)):
        if l[i].isdigit() or l[i] in ['+','-','*','/','^', '(', ')']:
            c.append(l[i])

    cc = ''.join(map(str, c)).split(' ')    

    s = rpn(cc[0])
    for x in s:
        if x == '+':
            g = polskiu.pop()
            z = polskiu.pop()
            polskiu.append(g + z)
        elif x == '-':
            g = polskiu.pop()
            z = polskiu.pop()
            polskiu.append(z - g)
        elif x == '*':
            g = polskiu.pop()
            z = polskiu.pop()
            polskiu.append(g * z)
        elif x == '#':
            polskiu.append(polskiu[-1])
        elif x == '@':
            polskiu.append(polskiu[-2])
            polskiu.append(polskiu[-2])
            polskiu.append(polskiu[-5])
            del polskiu[-4]
            del polskiu[-4]
            del polskiu[-4]
        elif x == '/':
            g = polskiu.pop()
            z = polskiu.pop()
            polskiu.append(z // g)
        elif x == '~':
            g = polskiu.pop()
            polskiu.append(-g)
        elif x == '!':
            g = polskiu.pop()
            polskiu.append(fac(g))
        else:
            polskiu.append(int(x))
    # print(polskiu[0])
    return polskiu[0]
# print(rpn("2+44*(56-12)/a-66"))

# zxc = ' '.join(map(str, rpn("2+44*(56-12)/a-66"))).split()

# print(zxc)