

"""
词法分析器
首先定义种别码
第一类：标识符（identifier）,种别码：0，属性值为字面值 letter(letter|digit)*
第二类：常数（constant），种别码：1，属性值为字面值 [+-]?(digit)+
第三类：保留字，种别码：2，属性值为字面值
第四类：界符，种别码：3，属性值为字面值
第五类：运算符，种别码：4，属性值字面值

保留字：
break case char const class continue double else extends float for
goto if int long new print return short sizeof static struct switch this
void while
界符：
'/*','//','(',')','{','}','[',']',''','"'
运算符：
'+','*','<','<=','>','>=','!=','=='

大致功能：
1.打开源文件，读取文件内容，直到遇到文件结束符
2.进行预处理，去除注释，以及影响程序执行的符号如换行符、回车符、制表符等，不要去除空格
3.从头到尾对源文件进行扫描，成功识别单词之后加如list，失败则返回错误
"""


"""
20201023
问题：
1.还没调试
2.没有检查界符与运算符是否都齐全了
3.是否完成oo形式的词法分析器
4.返回的常数token并不带符号
"""
import re

reserve_words = ['break','case','char','const','class','continue','double','else','extendes','float','for','goto','if','int','long','new','print','return','short','sizeof','static','struct','switch','this','void','while']
boundary = ['//','(',')','{','}','[',']','\'','"',';']
operator = ['+','*','<','<=','>','>=','!=','==','||','&&','|','&']



def scanner(str = ' ',p = 0):
    zimianzhi = ''
    while(p<len(str)):
        while str[p] is ' ':
            p += 1
        start = p
        if str[p].isalpha():
            while (str[p].isalnum()):
                p += 1
            zimianzhi = str[start:p]
            if (zimianzhi in reserve_words):
                list.append((2,zimianzhi))
            else:
                list.append((0,zimianzhi))
        elif str[p].isdigit():
            while(str[p].isdigit()):
                p += 1
            zimianzhi = str[start:p]
            list.append((1,zimianzhi))
        elif str[p] in boundary:
            if str[p] is '\/' and str[p+1] is '\/':
                p += 2
                list.append(3,'\/\/')
            else:
                list.append(3,str[p])
                p += 1
        elif str[p] in operator:
            if str[p] is '>' and str[p+1] is '=':
                p += 2
                list.append(4,'>=')
            elif str[p] is '<' and str[p+1] is '=':
                p += 2
                list.append(4,'<=')
            elif str[p] is '=' and str[p+1] is '=':
                p += 2
                list.append(4,'==')
            elif str[p] is '!' and str[p+1] is '=':
                p += 2
                list.append(4,'!=')
            elif str[p] is '|' and str[p+1] is '|':
                p += 2
                list.append(4,'!|')
            elif str[p] is '&' and str[p+1] is '&':
                p += 2
                list.append(4,'&&')
            else:
                list.append(4,str[p])
                p += 1
        else:
            raise Exception
    return

def lex(source):
    list = []
    with open(source) as f:
        for line in f:
            i,j = re.search(r'\/\/',line)
            i = i if i>0 else 0
            line_nocomment = line[i:].lstrip()
            scanner(line_nocomment)
    return list



