# 如果标识符 返回编号0
# 如果数字 返回编号1
# 如果其它 返回编号2
import lexer

# 对于所有变量池，名称：类型
# 全局变量
global_var_pool = {}

retract_layer = 0  # 缩进层次


# 变量池,管理变量
# class variable_pool:
#     Name_scope_Kind = {}
#
#     # layer从1开始
#     def add(self,name,kind,layer):
#         key = name + "_" + str(layer)
#         if key in self.Name_scope_Kind:
#             print("重复定义")
#             raise Exception
#         else:
#             self.Name_scope_Kind[key] = kind
#
#     def query(self,name,layer):
#         for i in range(layer):
#             key = name + "_" + str(layer-i)
#             if key in self.Name_scope_Kind:
#                 return self.Name_scope_Kind[key]
#         return None


# 类里的函数体
class func_structure:
    return_value = ""
    parameter_pool = {}

    # 构造函数 a(int,char) --> name a_int_char标识唯一性,只有构造函数可以允许相同的变量名
    def __init__(self, return_value, parameter_list):
        self.return_value = return_value
        for [par_name,par_kind] in parameter_list:
            self.parameter_pool[par_name] = par_kind



# 类结构，管理类
# 类内变量池、构造函数池、普通函数池、父类名
class class_structure:
    cla_var_pool = {}
    func_construct_pool = {}
    func_pool = {}
    parentName = None

    def __init__(self, cla_var_pool, func_construct_list, func_list, parentName = None):
        self.cla_var_pool = cla_var_pool
        self.parentName = parentName

        for [func_c_name, struc] in func_construct_list:
            if func_c_name in self.func_construct_pool:
                print("构造函数重复定义")
                raise Exception
            else:
                self.func_construct_pool[func_c_name] = struc
        for [func_name, struc] in func_list:
            if func_name in self.func_pool:
                print("函数重复定义")
                raise Exception
            else:
                self.func_pool[func_name] = struc

# 参数表
# return ind,parameter_list,post_name
def parameter(wordlist, ind):
    global retract_layer
    print("-"*retract_layer + "<参数表>")
    post_name = ""
    parameter_list = []

    retract_layer += 4
    while wordlist[ind][1] != ")":
        if wordlist[ind][1] == ",":
            ind += 1
        post_name = post_name + wordlist[ind][1]
        par_kind = wordlist[ind][1]
        ind += 1
        par_name = wordlist[ind][1]
        ind += 1
        print("-"*retract_layer + "<类型标识符>")
        print("-"*retract_layer + "<标识符>")
        parameter_list.append([par_name,par_kind])
    retract_layer -= 4
    return ind,parameter_list,post_name


def value_parameter(wordlist,ind):
    global retract_layer
    print("-"*retract_layer + "<值参数表>")
    retract_layer += 4

    if wordlist[ind][1]==")":
        print("-"*retract_layer + "<空>")

    else:

        ind = expression(wordlist, ind)
        while wordlist[ind][1] != ",":
            ind = expression(wordlist, ind)

    retract_layer -= 4
    return ind


# 函数调用
def call_func(wordlist, ind):
    global retract_layer
    print("-"*retract_layer + "<函数调用>")
    retract_layer +=4
    if wordlist[ind][0] == 0 and wordlist[ind+1][1] == "." and wordlist[ind+2][0] == 0:
        print("-"*retract_layer + "<标识符>")
        print("-"*retract_layer + "<标识符>")
        ind += 4
        ind = value_parameter(wordlist,ind)
        int += 1
    retract_layer -= 4
    return ind


# 因子
def factor(wordlist,ind):
    global retract_layer
    print("-"*retract_layer + "<因子>")
    retract_layer += 4

    if wordlist[ind][0] == 0 and wordlist[ind+1][1] != '.':  # 单个标识符
        ind += 1
        print("-"*retract_layer + "<标识符>")
    elif wordlist[ind][0] == 1:  # 整数
        print("-"*retract_layer + "<整数>")
        ind += 1
    elif wordlist[ind][1] == "'":  # 字符
        print("-"*retract_layer + "<字符>")
        ind += 3
    elif wordlist[ind][1] == "(":  # 表达式
        ind += 1
        ind = expression(wordlist,ind)
        ind += 1
    elif wordlist[ind][0] == 0 and wordlist[ind+1][1] == "." and wordlist[ind+2][0] == 0 and wordlist[ind+3][1] == "(":#有返回值函数调用
        ind = call_func(wordlist,ind)
    elif wordlist[ind][0] == 0 and wordlist[ind+1][1] == "." and wordlist[ind+2][0] == 0:
        print("-" * retract_layer + "<标识符>")
        print("-" * retract_layer + "<标识符>")
        ind += 3
    else:
        print("语法分析出错")
        raise Exception
    retract_layer -= 4
    return ind


# 项
def item(wordlist,ind):
    global retract_layer
    print("-"*retract_layer + "<项>")
    retract_layer += 4
    ind = factor(wordlist,ind)
    while wordlist[ind][1] == "*" or wordlist[ind][1] == "/":
        print("-"*retract_layer + "<乘法运算符>")
        ind += 1
        ind = factor(wordlist,ind)
    retract_layer -= 4
    return ind


# 表达式
def expression(wordlist,ind):
    global retract_layer
    print("-"*retract_layer + "<表达式>")
    retract_layer += 4
    if wordlist[ind][1] == "+" or wordlist[ind][1] == "-":
        ind += 1
        print("-"*retract_layer + "<加法运算符>")
        ind = item(wordlist, ind)
        while wordlist[ind][1] == "+" or wordlist[ind][1] == "-":
            print("-"*retract_layer + "<加法运算符>")
            ind += 1
            ind = item(wordlist, ind)
    else:
        ind = item(wordlist, ind)
        while wordlist[ind][1] == "+" or wordlist[ind][1] == "-":
            print("-"*retract_layer + "<加法运算符>")
            ind += 1
            ind = item(wordlist, ind)
    retract_layer -= 4
    return ind


# 语句
def statement(wordlist, ind):
    global retract_layer
    print("-"*retract_layer + "<语句>")
    # 条件语句 if
    # 赋值语句 标识符=
    # 函数调用语句 标识符.
    # 写语句 print
    # 空 ;
    # 返回语句 return
    retract_layer += 4
    # 空
    if wordlist[ind][1] == ";":
        print("-"*retract_layer + "<空>")
        ind += 1

    elif wordlist[ind][1] == "if":
        ind = condition_statement(wordlist, ind)

    elif wordlist[ind][1] == "print":
        ind = write_statement(wordlist, ind)

    elif wordlist[ind][1] == "return":
        ind = return_statement(wordlist, ind)

    elif wordlist[ind][0] == 0:
        if wordlist[ind+1][1] == "=":
            ind = assign_statement(wordlist, ind)

        elif wordlist[ind+1][1] == ".":
            ind = call_func(wordlist, ind)

        else:
            print("语法分析出错")
            raise Exception
    else:
        print("语法分析出错")
        raise Exception
    retract_layer -= 4
    return ind

#条件
def condition(wordlist, ind):
    global retract_layer
    print("-" * retract_layer + "<条件>")
    retract_layer += 4
    ind = expression(wordlist, ind)
    op = wordlist[ind][1]
    ind += 1
    if op == "<" or op == "<=" or op==">" or op==">=" or op=="!=" or op=="==":
        ind = expression(wordlist, ind)
    retract_layer -= 4
    return ind

# 条件语句
def condition_statement(wordlist,ind):
    global retract_layer
    print("-" * retract_layer + "<条件语句>")
    retract_layer += 4
    ind += 2
    ind = condition(wordlist, ind)
    ind += 1
    ind = statement(wordlist, ind)
    if wordlist[ind][1] == "else":
        ind += 1
        ind = statement(wordlist, ind)
    retract_layer -= 4
    return ind


# 写语句
def write_statement(wordlist, ind):
    global retract_layer
    print("-" * retract_layer + "<写语句>")
    ind += 2
    retract_layer += 4
    ind = expression(wordlist, ind)
    retract_layer -= 4
    ind += 1
    return ind

# 返回语句
def return_statement(wordlist, ind):
    global retract_layer
    print("-" * retract_layer + "<返回语句>")
    retract_layer += 4
    ind += 1
    if wordlist[ind][1]=="(":
        ind += 1
        ind = expression(wordlist, ind)
        ind += 1
    retract_layer -= 4
    return ind

# 赋值语句
def assign_statement(wordlist, ind):
    global retract_layer
    print("-" * retract_layer + "<赋值语句>")
    retract_layer += 4
    print("-" * retract_layer + "<标识符>")
    ind += 2
    ind = expression(wordlist, ind)
    retract_layer -= 4
    return ind


# 声明类变量
def define_cls_variable(wordlist, ind):
    global retract_layer
    class_var_pool = {}
    print("-"*retract_layer + "<类定义>")
    retract_layer += 4
    while wordlist[ind][0] == 0 and wordlist[ind+1][0] == 0 and wordlist[ind+2][1] == "=" and \
            wordlist[ind+3][1] == "new":

        print("-" * retract_layer + "<标识符>")
        print("-" * retract_layer + "<标识符>")
        kind = wordlist[ind][1]
        name = wordlist[ind+1][1]
        class_var_pool[name] = kind
        print("-" * retract_layer + "<标识符>")
        ind += 6
        ind = value_parameter(wordlist, ind)
        ind += 2
        if ind+3 >= len(wordlist)-1:
            break
    retract_layer -= 4
    return ind, class_var_pool


# 复合语句
# local_var_pool和global_var_pool用来检查变量的语义,都是字典 {varname:varkind}
def compound_statement(wordlist,ind,local_var_pool):
    global retract_layer
    print("-"*retract_layer + "<复合语句>")
    retract_layer += 4
    if wordlist[ind][1] == "int" or wordlist[ind][1] == "char":
        # 变量定义
        ind, var_pool = define_variable(wordlist,ind)  # 这里多了一个var_pool可以检查变量
    if wordlist[ind][0] == 0 and wordlist[ind+1][0] == 0 and wordlist[ind+2][1] == "=" and wordlist[ind+3][1] == "new":
        # 类定义
        ind, class_var_pool = define_cls_variable(wordlist, ind)


    while wordlist[ind][1] != "}":#复合语句未结束
        ind = statement(wordlist, ind)

    retract_layer -= 4
    # 结束时 ind--》"}"
    return ind


# 返回 ind,func_construct_list
# [func_c_name,struc] in func_construct_list
# 构造函数变量来源于：全局变量、构造函数参数列表、类内部变量
def construct_define(wordlist,name, ind, class_var_pool):
    global retract_layer
    func_construct_list = []
    while wordlist[ind][1] == name:
        print("-"*retract_layer + "<构造函数定义>")
        retract_layer += 4
        print("-"*retract_layer + "<标识符>")
        ind += 2
        # 参数 post_name是后缀
        ind, parameter_list, post_name = parameter(wordlist,ind)
        new_name = name + "_" + post_name
        ind += 2

        local_var_pool = class_var_pool
        for [par_name,par_kind] in parameter_list:
            local_var_pool[par_name] = par_kind
        # 复合语句
        ind = compound_statement(wordlist, ind, local_var_pool)
        # ind指向“}”
        ind += 1
        func_struct = func_structure("", parameter_list)
        func_construct_list.append([new_name, func_struct])
        retract_layer -= 4
    return ind,func_construct_list


# 返回ind,func_pool [[func_name,struc],]
def func_define(wordlist,ind,class_var_pool):
    global retract_layer
    func_list = []
    while wordlist[ind][1] != "}":
        print("-"*retract_layer + "<函数定义>")
        retract_layer += 4

        return_value = wordlist[ind][1]
        print("-"*retract_layer + "<标识符>")
        name = wordlist[ind+1][1]
        ind += 3
        # 参数
        ind, parameter_list, post_name = parameter(wordlist, ind)
        ind += 2

        local_var_pool = class_var_pool
        for [par_name, par_kind] in parameter_list:
            local_var_pool[par_name] = par_kind
        # 复合语句
        ind = compound_statement(wordlist, ind, local_var_pool)
        # ind指向“}”
        ind += 1
        func_struct = func_structure(return_value, parameter_list)
        func_list.append([name, func_struct])
        retract_layer -= 4
    return ind, func_list


#  ind指向class
#  cla_var_pool = variable_pool()
#  func_construct_pool = {}
#  func_pool = {}
#  parentName = None
def define_class(wordlist, ind):
    global retract_layer
    cla_structure_list = []
    while wordlist[ind][1] == "class":
        print("-"*retract_layer + "<类声明>")
        ind += 1
        retract_layer += 4
        print("-"*retract_layer + "<标识符>")
        name = wordlist[ind][1]
        ind += 1
        if wordlist[ind][1] == "extends":
            parent_name = wordlist[ind+1][1]
            print("-" * retract_layer + "<标识符>")
            ind += 2
        else:
            parent_name = None
        ind += 1
        # 变量定义
        ind, class_var_pool = define_variable(wordlist, ind)
        # 构造函数定义
        ind, func_construct_list = construct_define(wordlist, name, ind, class_var_pool)
        if wordlist[ind][1] != "}":  # 有普通函数
            ind, func_list = func_define(wordlist, ind, class_var_pool)
        else:
            func_list = []
        ind += 1
        cla_structure_list.append(class_structure(class_var_pool, func_construct_list, func_list, parent_name))
        retract_layer -= 4
    return ind, cla_structure_list


def define_variable(wordlist,ind):
    global retract_layer
    print("-"*retract_layer + "<变量定义>")
    retract_layer += 4
    var_pool = {}
    while wordlist[ind][1] == "int" or wordlist[ind][1] == "char":
        if wordlist[ind][1] == "int":
            kind = "int"
            while wordlist[ind][1] != ";":
                ind += 1
                name = wordlist[ind][1]
                print("-"*retract_layer + "<标识符>")
                var_pool[name] = kind
                ind += 2
                # 数字
                print("-"*retract_layer + "<整数>")
                if wordlist[ind][0] != 1:  # 整数带符号
                    ind += 2
                else:
                    ind += 1
        else:
            kind = "char"
            while wordlist[ind][1] != ";":
                ind += 1
                name = wordlist[ind][1]
                print("-" * retract_layer + "<标识符>")
                var_pool[name] = kind
                ind += 5
                print("-"*retract_layer + "<字符>")
        ind += 1

        if ind >= len(wordlist):
            break
    retract_layer -= 4
    return ind, var_pool


def define_main(wordlist, ind):
    global retract_layer
    ind += 3
    print("-"*retract_layer + "<主函数>")
    retract_layer += 4
    ind = compound_statement(wordlist, ind, {})
    retract_layer -= 4
    return ind


def grammar(wordlist):
    ind = 0
    # 变量定义
    if wordlist[ind][1] == 'int' or wordlist[ind][1] == 'char':
        ind, global_var_pool = define_variable(wordlist, ind)
        ind, class_pool = define_class(wordlist, ind)
        ind = define_main(wordlist, ind)
    # 类声明
    elif wordlist[ind][1] == 'class':
        ind,class_pool = define_class(wordlist, ind)
        ind = define_main(wordlist, ind)
    # 主函数
    elif wordlist[ind][1]=='void':
        ind = define_main(wordlist, ind)
    else:
        print("语法分析出错")
        raise Exception


if __name__ =="__main__":
    lex = lexer.lex_test("int a = 1,b = 2,c = 3;char a1 = 'a',_b = '2',_c = 'c';int a4 = 1,b4 = 2,c4 = 3;class temp{int b=1;}void main{temp a = new a();"
                         "print(a+b);return;}")
    grammar(lexer.wordlist)
