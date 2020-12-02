# 如果标识符 返回编号0
# 如果数字 返回编号1
# 如果其它 返回编号2
import lexer

# 对于所有变量池，名称：类型
# 全局变量
global_var_pool = {}

retract_layer = 0  # 缩进层次


# 变量堆栈
class Stack(object):
    # 初始化栈为空列表
    def __init__(self):
        self.items = []

    # 判断栈是否为空，返回布尔值
    def is_empty(self):
        return self.items == []

    # 返回栈顶元素
    def peek(self):
        return self.items[len(self.items) - 1]

    # 返回栈的大小
    def size(self):
        return len(self.items)

    # 把新的元素堆进栈里面
    def push(self, i):
        self.items.append(i)

    # 把栈顶元素丢出去
    def pop(self):
        return self.items.pop()

    def reverse_query(self,i):
        for ind, j in enumerate(self.items[::-1]):
            if i in j:
                if ind == 0:
                    return i + " 是<复合语句>内定义的变量"
                elif ind == 1:
                    return i + " 是<函数定义>内定义的变量"
                elif ind == 2:
                    return i + " 是<类声明>内定义的变量"
                else:
                    return i + " 是<程序>内定义的变量"

        return i + " 是未定义变量"

    def reverse_find_kind_by_name(self, i):
        for ind, j in enumerate(self.items[::-1]):
            if i in j:
                return j[i]

        return None


# 本地变量堆栈
var_local_stack = Stack()
# 类变量堆栈
cls_var_stack = Stack()
# 类信息列表
class_pool = {}
# 变量语义分析
var_analysis = []
# 类语义分析
cls_analysis = []


def print_analysis():
    global var_analysis
    global cls_analysis
    print("\n"*3)
    print("----------普通变量（非类对象）相关分析-----------")
    print("\n".join(var_analysis))
    print("\n" * 3)
    print("----------类对象相关分析-----------")
    print("\n".join(cls_analysis))


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

    def __init__(self, cla_var_pool, func_construct_pool, func_pool, parentName = None):
        self.cla_var_pool = cla_var_pool
        self.parentName = parentName
        self.func_construct_pool = func_construct_pool
        self.func_pool = func_pool

    def check_in_con_pool(self,func_name):
        if func_name in self.func_construct_pool:
            return True
        else:
            return False

    def check_para(self,para):
        if para in self.cla_var_pool:
            return True
        else:
            return False

    def check_func(self,fuc_name):
        global class_pool
        if fuc_name in self.func_pool:
            return True
        if self.parentName is not None:
            return class_pool[self.parentName].check_func(fuc_name)
        else:
            return False


# 参数表
# return ind,parameter_list,post_name
def parameter(wordlist, ind):
    global retract_layer
    print("-"*retract_layer + "<参数表>")
    post_name = 0
    parameter_list = []

    retract_layer += 4
    while wordlist[ind][1] != ")":
        if wordlist[ind][1] == ",":
            ind += 1
        post_name = post_name + 1
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
    post_name = 0
    if wordlist[ind][1]==")":
        print("-"*retract_layer + "<空>")

    else:

        ind = expression(wordlist, ind)
        post_name += 1
        while wordlist[ind][1] != ",":
            ind = expression(wordlist, ind)
            post_name += 1
    retract_layer -= 4
    # ind += 2
    return ind,post_name


# 函数调用
def call_func(wordlist, ind):
    global retract_layer
    global cls_analysis
    global class_pool
    global cls_var_stack

    print("-"*retract_layer + "<函数调用>")
    retract_layer +=4
    if wordlist[ind][0] == 0 and wordlist[ind+1][1] == "." and wordlist[ind+2][0] == 0:
        print("-"*retract_layer + "<标识符>")
        print("-"*retract_layer + "<标识符>")

        class_name = wordlist[ind][1]
        variable_name = wordlist[ind+2][1]

        ind += 4
        ind, post_name = value_parameter(wordlist, ind)

        #  检查变量是否存在
        kind = cls_var_stack.reverse_find_kind_by_name(class_name)
        if kind is None:
            check_str = wordlist[ind][1] + "该变量不存在"
        else:
            if class_pool[kind].check_func(variable_name + "_" + str(post_name)):
                check_str = "变量" + class_name + ",函数" + variable_name + "存在且符合要求"
            else:
                check_str = "变量" + class_name + "存在,函数" + variable_name + "不存在or不符合要求"
        cls_analysis.append(check_str)





        ind += 2

    retract_layer -= 4
    return ind


# 因子
def factor(wordlist,ind):
    global retract_layer
    global var_analysis
    global cls_analysis
    global class_pool
    global cls_var_stack
    global var_local_stack

    print("-"*retract_layer + "<因子>")
    retract_layer += 4

    if wordlist[ind][0] == 0 and wordlist[ind+1][1] != '.':  # 单个标识符
        var_analysis.append(var_local_stack.reverse_query(wordlist[ind][1]))
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
        kind = cls_var_stack.reverse_find_kind_by_name(wordlist[ind][1])

        if kind is None:
            check_str = wordlist[ind][1]+ "该变量不存在"
        else:
            if class_pool[kind].check_para(wordlist[ind+2][1]):
                check_str = "变量"+wordlist[ind][1]+"参数"+wordlist[ind+2][1]+"存在"
            else:
                check_str = "变量" + wordlist[ind][1] + "存在，参数" + wordlist[ind + 2][1] + "不存在"
        cls_analysis.append(check_str)

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
    ind += 2
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
    ind += 1
    return ind


# 定义类变量
def define_cls_variable(wordlist, ind):
    global retract_layer
    global cls_analysis
    global class_pool
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
        ind, post_name = value_parameter(wordlist, ind)


        # 检查类是否存在,参数是否符合要求
        if kind in class_pool:
            check_str = kind + "类型存在，"
            new_construct_name = kind + "_" + str(post_name)

            if class_pool[kind].check_in_con_pool(new_construct_name):
                check_str = check_str + "构造函数符合要求"
            else:
                check_str = check_str + "构造函数不符合要求"
        else:
            check_str = kind + "不存在 "

        cls_analysis.append(check_str)

        ind += 2

        if ind+3 >= len(wordlist)-1:
            break
    retract_layer -= 4
    return ind, class_var_pool


# 复合语句
# local_var_pool和global_var_pool用来检查变量的语义,都是字典 {varname:varkind}
def compound_statement(wordlist,ind):
    global retract_layer
    global var_local_stack
    global cls_var_stack

    print("-"*retract_layer + "<复合语句>")
    retract_layer += 4
    class_var_pool = {}
    var_pool = {}
    if wordlist[ind][1] == "int" or wordlist[ind][1] == "char":
        # 变量定义
        ind, var_pool = define_variable(wordlist,ind)  # 这里多了一个var_pool可以检查变量

    var_local_stack.push(var_pool)  # 函数内定义
    if wordlist[ind][0] == 0 and wordlist[ind+1][0] == 0 and wordlist[ind+2][1] == "=" and wordlist[ind+3][1] == "new":
        # 类定义
        ind, class_var_pool = define_cls_variable(wordlist, ind)#class_var_pool={name:kind}

    cls_var_stack.push(class_var_pool)

    while wordlist[ind][1] != "}":#复合语句未结束
        ind = statement(wordlist, ind)

    var_local_stack.pop()  # 把函数内部定义的变量给去除了
    cls_var_stack.pop()
    retract_layer -= 4
    # 结束时 ind--》"}"
    return ind


# 返回 ind,func_construct_list
# [func_c_name,struc] in func_construct_list
# 构造函数变量来源于：全局变量、构造函数参数列表、类内部变量
def construct_define(wordlist,name, ind, class_var_pool):
    global retract_layer
    global var_local_stack
    var_local_stack.push(class_var_pool)  # 类内变量
    new_name = name + "_" + "0"
    func_construct_pool = {}
    func_construct_pool[new_name] = func_structure("", [])
    while wordlist[ind][1] == name:
        print("-"*retract_layer + "<构造函数定义>")
        retract_layer += 4
        print("-"*retract_layer + "<标识符>")
        ind += 2
        # 参数 post_name是后缀
        ind, parameter_list, post_name = parameter(wordlist,ind)
        new_name = name + "_" + str(post_name)
        ind += 2

        local_var_pool = {}
        for [par_name,par_kind] in parameter_list:
            local_var_pool[par_name] = par_kind
        var_local_stack.push(local_var_pool)  # 函数参数

        # 复合语句
        ind = compound_statement(wordlist, ind)
        # ind指向“}”
        ind += 1
        var_local_stack.pop()  # 把函数参数给弹出了
        func_struct = func_structure("", parameter_list)
        func_construct_pool[new_name] = func_struct
        retract_layer -= 4
    var_local_stack.pop()  # 把类内变量弹出了
    return ind,func_construct_pool


# 返回ind,func_pool [[func_name,struc],]
def func_define(wordlist,ind,class_var_pool):
    global retract_layer
    global var_local_stack

    var_local_stack.push(class_var_pool)  # 类内变量
    func_pool = {}
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
        new_name = name + "_" + str(post_name)
        local_var_pool = {}
        for [par_name, par_kind] in parameter_list:
            local_var_pool[par_name] = par_kind
        # 复合语句
        var_local_stack.push(local_var_pool)  # 函数参数
        ind = compound_statement(wordlist, ind)
        # ind指向“}”
        ind += 1
        func_struct = func_structure(return_value, parameter_list)
        func_pool[new_name] = func_struct

        var_local_stack.pop()  # 把函数参数给弹出了

        retract_layer -= 4

    var_local_stack.pop()  # 把类内变量弹出了
    return ind, func_pool


#  ind指向class
#  cla_var_pool = variable_pool()
#  func_construct_pool = {}
#  func_pool = {}
#  parentName = None
def define_class(wordlist, ind):
    global retract_layer
    cla_structure_pool = {}
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
        ind, func_construct_pool = construct_define(wordlist, name, ind, class_var_pool)
        if wordlist[ind][1] != "}":  # 有普通函数
            ind, func_pool = func_define(wordlist, ind, class_var_pool)
        else:
            func_pool = {}
        ind += 1
        cla_structure_pool[name]=class_structure(class_var_pool, func_construct_pool, func_pool, parent_name)
        retract_layer -= 4
    return ind, cla_structure_pool


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
    ind = compound_statement(wordlist, ind)
    retract_layer -= 4
    return ind


def grammar(wordlist):
    global global_var_pool
    global class_pool
    global var_local_stack

    ind = 0
    # 变量定义
    if wordlist[ind][1] == 'int' or wordlist[ind][1] == 'char':
        ind, global_var_pool = define_variable(wordlist, ind)  # global_var_pool = {name:kind}
        var_local_stack.push(global_var_pool)
        ind, class_pool = define_class(wordlist, ind)  # class_pool = [class_structure,]
        ind = define_main(wordlist, ind)
    # 类声明
    elif wordlist[ind][1] == 'class':
        var_local_stack.push(global_var_pool)
        ind,class_pool = define_class(wordlist, ind)
        ind = define_main(wordlist, ind)
    # 主函数
    elif wordlist[ind][1]=='void':
        var_local_stack.push(global_var_pool)
        ind = define_main(wordlist, ind)
    else:
        print("语法分析出错")
        raise Exception

    print_analysis()

if __name__ =="__main__":
    lex = lexer.lex_test("int ab=10;class a{void bb(){print(ab+2);}}class b extends a{void c(){print(1+2);}}void main{b t = new b(); t.bb();ab=20;return;}")
    grammar(lexer.wordlist)
