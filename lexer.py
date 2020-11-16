# -!- coding: utf-8 -!-
reserve_words = ['char','class','else','extends','if','int','new','print','return','this','void','main']
boundary = ['(',')','{','}',"'",".",';',","]
operator = ['+','*','<','<=','>','>=','!=','==','-','=',"!"]
wordlist = []

#如果标识符 返回编号0
#如果数字 返回编号1
#如果其它 返回编号2

def scanner(line,p = 0):
    line = line+" " #防止溢出
    while p<len(line)-1:
        while line[p] == ' ':
            p += 1
        start = p
        if line[p].isalpha() or line[p] == '_':
            if line[p] == '_':
                p += 1
            while line[p].isalnum():
                p += 1
            tempstr = line[start:p]
            if tempstr in reserve_words:
                wordlist.append([2, tempstr])
            else:
                wordlist.append([0, tempstr])
        #数字
        elif line[p].isdigit():
            if line[p]=='0' and line[p+1].isdigit():
                print("词法分析出错")
                raise Exception
            while line[p].isdigit():
                p += 1
            tempstr = line[start:p]
            wordlist.append([1, int(tempstr)])
        elif line[p] in boundary:
            wordlist.append([2, line[p]])
            p += 1
        elif line[p] in operator:
            if line[p] == '>' and line[p+1] == '=':
                p += 2
                wordlist.append([2,'>='])
            elif line[p] == '<' and line[p+1] == '=':
                p += 2
                wordlist.append([2,'<='])
            elif line[p] == '=' and line[p+1] == '=':
                p += 2
                wordlist.append([2,'=='])
            elif line[p] == '!' and line[p+1] == '=':
                p += 2
                wordlist.append([2,'!='])
            elif line[p] == '!' and line[p+1] != '=':
                print("词法分析出错")
                raise Exception
            else:
                wordlist.append([2, line[p]])
                p += 1
        else:
            print("词法分析出错")
            raise Exception
    return

def lex(source):
    with open(source) as f:
        for line in f:
            scanner(line)

def lex_test(source):
    scanner(source)





