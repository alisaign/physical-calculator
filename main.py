import pandas as pd

def tokenize(s):
    result = []
    var = ""
    for c in s:
        if c in "()+-/**2":
            if var:
                result.append((var, "var"))
                var = ""
            result.append((c, "op"))
        else:
            var += c
    if var:
        result.append((var, "var"))
    return result

def get_vars(formula):
    el = tokenize(formula)
    vars = []
    for t in el:
        if t[1] == "var":
            vars.append(t[0])
    return vars

def extend(a):
    lst = list(a)
    formula = lst[1]
    el = tokenize(formula)
    vars = []
    for t in el:
        if t[1] == "var":
            vars.append(t[0])
    lst.append(vars)
    return lst

def rang(s, vars): # считает с какой вероятностью данная формула подходит и возвращает число
    k = 0
    for c in s:
        if c in "()+-/**2":
            continue
        elif c in vars:
            k += 1
        else:
            k -= 1
    return k

def find_new_x(s, vars): # ищет какие переменные в формуле неизвестны и возвращает их список
    need_find = []
    for c in s:
        if c in "()+-/**2":
            continue
        elif c in vars:
            continue
        else:
            need_find.append(c)
    return need_find

def rang_with_vars(s):
    return rang(s[1], vars)

def check(candidate, recursion): # функция для проверки формулы - кандидата
    argnames = candidate[2]
    formula = candidate[1]
    children = []
    for var in argnames:
        (result, steps) = main_function(var, recursion)
        if not result:
            return (False, ())
        if result == var:
            children.append(steps)
            continue
        children.append(steps)
        formula = formula.replace(var, "("+result+")")
    return (formula, (candidate[0], candidate[1], children))

def main_function(x, recursion):

    if x in vars:
        return (x, (x, "из дано", []))                  # проверка дана ли эта переменная

    if recursion > 3:                                   # чтобы не было зацикливаний
        return (False, ())

    xvars = []

    for line in data:                                    # список со всеми формулами
        if line[0] == x:                                 # ищем переменную, которую надо найти
            xvars.append(line)                           # список с формулами для неизвестной переменной

    xvars.sort(key=rang_with_vars, reverse=True)
    print(xvars)# список в котором формулы отсортированы по вероятности использования

    for candidate in xvars:                              # проверка каждой формулы из списка
        (result, steps) = check(candidate, recursion+1)
        print(steps)# рекурсивная функция
        if result:                                       # для переменной удалось выразить все неизвестные через дано
            return (result, steps)                       # формирование решения
    return (False, ())                                   # не удалось найти все неизвестные

def format(cort, tabs):
    a, b, c = cort
    if b == "из дано":
        word = " "
    else:
        word = " = "
    print(tabs, a+word+b)
    for x in c:
        format(x, tabs + "\t")

df = pd.read_csv('формулы.txt', delimiter='\t') #читаем формулы в список
data = [tuple(extend(x)) for x in df.values]
#print(data)

#x = input("Введите переменную которую нужно найти-->")
#vars = input("введите переменные, которые даны, через пробел-->")
x = "kpd"
vars = "t m h U I g"
vars = vars.split()
#print(x, vars, sep = '\n')
x1 = x

(res, steps) = main_function(x, 0)
if res:
    print("Вы спасены! Решение нашлось")
    print(x1+" =", res)
    format(steps, " ")
else:
    print("Ничего не нашлось. Вам грозит пара(")