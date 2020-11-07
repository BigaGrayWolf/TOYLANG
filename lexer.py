

"""
�ʷ�������
���ȶ����ֱ���
��һ�ࣺ��ʶ����identifier��,�ֱ��룺0������ֵΪ����ֵ letter(letter|digit)*
�ڶ��ࣺ������constant�����ֱ��룺1������ֵΪ����ֵ [+-]?(digit)+
�����ࣺ�����֣��ֱ��룺2������ֵΪ����ֵ
�����ࣺ������ֱ��룺3������ֵΪ����ֵ
�����ࣺ��������ֱ��룺4������ֵ����ֵ

�����֣�
break case char const class continue double else extends float for
goto if int long new print return short sizeof static struct switch this
void while
�����
'/*','//','(',')','{','}','[',']',''','"'
�������
'+','*','<','<=','>','>=','!=','=='

���¹��ܣ�
1.��Դ�ļ�����ȡ�ļ����ݣ�ֱ�������ļ�������
2.����Ԥ����ȥ��ע�ͣ��Լ�Ӱ�����ִ�еķ����绻�з����س������Ʊ���ȣ���Ҫȥ���ո�
3.��ͷ��β��Դ�ļ�����ɨ�裬�ɹ�ʶ�𵥴�֮�����list��ʧ���򷵻ش���
"""


"""
20201023
���⣺
1.��û����
2.û�м������������Ƿ���ȫ��
3.�Ƿ����oo��ʽ�Ĵʷ�������
4.���صĳ���token����������
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



