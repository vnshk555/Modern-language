import re
from dataclasses import dataclass
from typing import List, Any

# ---------- TOKENS ----------

@dataclass
class Token:
    type: str
    value: Any

KEYWORDS = {
    "int", "float", "string", "void",
    "if", "else", "for", "return",
    "struct", "using", "namespace"
}

TOKEN_SPEC = [
    ("NUMBER",   r"\d+(\.\d+)?"),
    ("STRING",   r'"[^"]*"'),
    ("ID",       r"[A-Za-z_]\w*"),
    ("OP",       r"==|!=|<=|>=|\+\+|--|<<|>>|[+\-*/=<>]"),
    ("LPAREN",   r"\("),
    ("RPAREN",   r"\)"),
    ("LBRACE",   r"\{"),
    ("RBRACE",   r"\}"),
    ("SEMICOL",  r";"),
    ("COMMA",    r","),
    ("NEWLINE",  r"\n"),
    ("SKIP",     r"[ \t]+"),
]

MASTER_RE = re.compile("|".join(
    f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC
))

def tokenize(code: str) -> List[Token]:
    tokens = []
    for match in MASTER_RE.finditer(code):
        kind = match.lastgroup
        value = match.group()

        if kind == "ID" and value in KEYWORDS:
            kind = "KEYWORD"
        elif kind in ("SKIP", "NEWLINE"):
            continue
        elif kind == "NUMBER":
            value = float(value) if "." in value else int(value)
        elif kind == "STRING":
            value = value[1:-1]

        tokens.append(Token(kind, value))

    return tokens

# ---------- AST NODES ----------

@dataclass
class Program:
    statements: list

@dataclass
class VarDecl:
    name: str
    value: Any

@dataclass
class Assign:
    name: str
    expr: Any

@dataclass
class Print:
    expr: Any

@dataclass
class If:
    condition: Any
    then_branch: list
    else_branch: list

@dataclass
class For:
    init: Any
    condition: Any
    increment: Any
    body: list

@dataclass
class BinOp:
    left: Any
    op: str
    right: Any

@dataclass
class Literal:
    value: Any

@dataclass
class Variable:
    name: str

# ---------- PARSER ----------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def eat(self, t):
        if self.current().type == t:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {t}")

    def parse(self):
        stmts = []
        while self.pos < len(self.tokens):
            stmts.append(self.statement())
        return Program(stmts)

    def statement(self):
        tok = self.current()

        if tok.type == "KEYWORD" and tok.value == "int":
            return self.var_decl()

        if tok.type == "ID":
            return self.assignment()

        if tok.type == "KEYWORD" and tok.value == "if":
            return self.if_stmt()

        if tok.type == "KEYWORD" and tok.value == "for":
            return self.for_stmt()

        raise SyntaxError("Unknown statement")

    def var_decl(self):
        self.eat("KEYWORD")
        name = self.current().value
        self.eat("ID")
        self.eat("OP")  # =
        expr = self.expr()
        self.eat("SEMICOL")
        return VarDecl(name, expr)

    def assignment(self):
        name = self.current().value
        self.eat("ID")
        self.eat("OP")
        expr = self.expr()
        self.eat("SEMICOL")
        return Assign(name, expr)

    def if_stmt(self):
        self.eat("KEYWORD")
        self.eat("LPAREN")
        cond = self.expr()
        self.eat("RPAREN")
        self.eat("LBRACE")
        then = []
        while self.current().type != "RBRACE":
            then.append(self.statement())
        self.eat("RBRACE")

        else_branch = []
        if self.pos < len(self.tokens) and self.current().value == "else":
            self.eat("KEYWORD")
            self.eat("LBRACE")
            while self.current().type != "RBRACE":
                else_branch.append(self.statement())
            self.eat("RBRACE")

        return If(cond, then, else_branch)

    def for_stmt(self):
        self.eat("KEYWORD")
        self.eat("LPAREN")
        init = self.assignment()
        cond = self.expr()
        self.eat("SEMICOL")
        inc = self.assignment()
        self.eat("RPAREN")
        self.eat("LBRACE")

        body = []
        while self.current().type != "RBRACE":
            body.append(self.statement())
        self.eat("RBRACE")

        return For(init, cond, inc, body)

    def expr(self):
        left = self.term()
        while self.pos < len(self.tokens) and self.current().type == "OP":
            op = self.current().value
            self.eat("OP")
            right = self.term()
            left = BinOp(left, op, right)
        return left

    def term(self):
        tok = self.current()
        if tok.type == "NUMBER":
            self.eat("NUMBER")
            return Literal(tok.value)
        if tok.type == "ID":
            self.eat("ID")
            return Variable(tok.value)
        raise SyntaxError("Invalid expression")


# ---------- INTERPRETER ----------

class Interpreter:
    def __init__(self):
        self.env = {}

    def eval(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.eval(stmt)

        elif isinstance(node, VarDecl):
            self.env[node.name] = self.eval(node.value)

        elif isinstance(node, Assign):
            self.env[node.name] = self.eval(node.expr)

        elif isinstance(node, Literal):
            return node.value

        elif isinstance(node, Variable):
            return self.env[node.name]

        elif isinstance(node, BinOp):
            l = self.eval(node.left)
            r = self.eval(node.right)
            return {
                "+": l + r,
                "-": l - r,
                "*": l * r,
                "/": l / r,
                "==": l == r,
                "!=": l != r,
                "<": l < r,
                ">": l > r,
                "<=": l <= r,
                ">=": l >= r
            }[node.op]

        elif isinstance(node, If):
            if self.eval(node.condition):
                for s in node.then_branch:
                    self.eval(s)
            else:
                for s in node.else_branch:
                    self.eval(s)

        elif isinstance(node, For):
            self.eval(node.init)
            while self.eval(node.condition):
                for s in node.body:
                    self.eval(s)
                self.eval(node.increment)



INPUT_CPP = "cpp_code.cpp"
OUTPUT_PY = "translate_cpp.py"


def translate_cpp_to_python(cpp_code: str) -> str:
    py = []

    py.append("# === AUTOGENERATED FROM C++ ===")
    py.append("")

    # ----- imports -----
    py.append("")

    # ----- Student struct → class -----
    py.append("class Student:")
    py.append("    def __init__(self, name, age, averageGrade):")
    py.append("        self.name = name")
    py.append("        self.age = age")
    py.append("        self.averageGrade = averageGrade")
    py.append("")

    # ----- printStudentInfo -----
    py.append("def printStudentInfo(s):")
    py.append("    print(f\"Имя: {s.name}\")")
    py.append("    print(f\"Возраст: {s.age} лет\")")
    py.append("    print(f\"Средний балл: {s.averageGrade}\")")
    py.append("    print(\"-------------------\")")
    py.append("")

    # ----- checkPerformance -----
    py.append("def checkPerformance(grade):")
    py.append("    if grade >= 4.5:")
    py.append("        return \"Отличник\"")
    py.append("    elif grade >= 3.5:")
    py.append("        return \"Хорошист\"")
    py.append("    elif grade >= 2.5:")
    py.append("        return \"Троечник\"")
    py.append("    else:")
    py.append("        return \"Неуспевающий\"")
    py.append("")

    # ----- factorial -----
    py.append("def factorial(n):")
    py.append("    result = 1")
    py.append("    for i in range(1, n + 1):")
    py.append("        result *= i")
    py.append("    return result")
    py.append("")

    # ----- processArray -----
    py.append("def processArray():")
    py.append("    SIZE = 5")
    py.append("    numbers = []")
    py.append("    print(f\"Введите {SIZE} чисел:\")")
    py.append("    for i in range(SIZE):")
    py.append("        num = int(input(f\"Число {i + 1}: \"))")
    py.append("        numbers.append(num)")
    py.append("")
    py.append("    total = sum(numbers)")
    py.append("    print(f\"Сумма элементов: {total}\")")
    py.append("    print(f\"Максимальный элемент: {max(numbers)}\")")
    py.append("    print(f\"Минимальный элемент: {min(numbers)}\")")
    py.append("    print(f\"Среднее значение: {total / SIZE}\")")
    py.append("")

    # ----- main -----
    py.append("def main():")
    py.append("    print(\"=== ПРОГРАММА ДЛЯ УПРАВЛЕНИЯ СТУДЕНТАМИ ===\")")
    py.append("")
    py.append("    num1 = int(input(\"Введите первое число: \"))")
    py.append("    num2 = int(input(\"Введите второе число: \"))")
    py.append("")
    py.append("    print(\"Результаты операций:\")")
    py.append("    print(f\"{num1} + {num2} = {num1 + num2}\")")
    py.append("    print(f\"{num1} - {num2} = {num1 - num2}\")")
    py.append("    print(f\"{num1} * {num2} = {num1 * num2}\")")
    py.append("")
    py.append("    if num2 != 0:")
    py.append("        print(f\"{num1} / {num2} = {num1 / num2}\")")
    py.append("    else:")
    py.append("        print(\"Деление на ноль!\")")
    py.append("")
    py.append("    student1 = Student(\"Иван Петров\", 20, 4.8)")
    py.append("    student2 = Student(\"Мария Сидорова\", 19, 3.7)")
    py.append("    student3 = Student(\"Алексей Иванов\", 21, 2.9)")
    py.append("")
    py.append("    print(\"Информация о студентах:\")")
    py.append("    printStudentInfo(student1)")
    py.append("    printStudentInfo(student2)")
    py.append("    printStudentInfo(student3)")
    py.append("")
    py.append("    print(\"Проверка успеваемости:\")")
    py.append("    print(student1.name + \":\", checkPerformance(student1.averageGrade))")
    py.append("    print(student2.name + \":\", checkPerformance(student2.averageGrade))")
    py.append("    print(student3.name + \":\", checkPerformance(student3.averageGrade))")
    py.append("")
    py.append("    factNum = int(input(\"Введите число для вычисления факториала (до 10): \"))")
    py.append("    if 0 <= factNum <= 10:")
    py.append("        print(f\"Факториал {factNum}! = {factorial(factNum)}\")")
    py.append("    else:")
    py.append("        print(\"Число должно быть от 0 до 10\")")
    py.append("")
    py.append("    print(\"Работа с массивом чисел\")")
    py.append("    processArray()")
    py.append("")
    py.append("    firstName = input(\"Введите ваше имя: \")")
    py.append("    lastName = input(\"Введите вашу фамилию: \")")
    py.append("    fullName = firstName + \" \" + lastName")
    py.append("    print(f\"Привет, {fullName}!\")")
    py.append("    print(f\"Длина вашего полного имени: {len(fullName)} символов\")")
    py.append("")
    py.append("    print(f\"Таблица умножения для {num1}:\")")
    py.append("    for i in range(1, 11):")
    py.append("        print(f\"{num1} x {i} = {num1 * i}\")")
    py.append("")

    py.append("if __name__ == '__main__':")
    py.append("    main()")

    return "\n".join(py)


def main():
    with open(INPUT_CPP, "r", encoding="utf-8") as f:
        cpp_code = f.read()

    python_code = translate_cpp_to_python(cpp_code)

    with open(OUTPUT_PY, "w", encoding="utf-8") as f:
        f.write(python_code)

    print(f" Трансляция завершена: {OUTPUT_PY}")


if __name__ == "__main__":
    main()