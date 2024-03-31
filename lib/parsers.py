from lib.lexica import MyLexer
from lib.memory import Memory
from lib.sly import Parser

class MyParser(Parser):
    debugfile = 'parser.out'
    start = 'statement'
    # Get the token list from the lexer (required)
    tokens = MyLexer.tokens
    precedence = (
        ('left', TIMES, DIVIDE),
        ('left', "+", MINUS),
        ('right', UMINUS),
        )

    def __init__(self):
        self.memory:Memory = Memory()

    @_('NAME ASSIGN expr')
    def statement(self, p):
        var_name = p.NAME
        value = p.expr
        self.memory.set(variable_name=var_name,value=value, data_type=type(value))
        # Note that I did not return anything

    @_('expr')
    def statement(self, p) -> int:
        return p.expr

    # The example with literals
    @_('expr "+" expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    # The example with normal token
    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)
    
    def pre_fix_expr(self, input_text):
        tokens = input_text.split()
        prefix = []
        operator_stack = []
        precedence_dict = {}

        for associativity, *ops in self.precedence:
            for op in ops:
                precedence_dict[op] = (associativity, len(ops))
        for token in reversed(list(tokens)):
            if token.isdigit():
                prefix.append(token)
            elif token in precedence_dict:
                while (operator_stack and
                    precedence_dict[token] <= precedence_dict[operator_stack[-1]]):
                    prefix.append(operator_stack.pop())
                operator_stack.append(token)

        while operator_stack:
            prefix.append(operator_stack.pop())
        prefix.reverse()
        prefix_str = ' '.join(prefix)

        return prefix_str
    
    def post_fix_expr(self, expression):
        operator_stack = []
        postfix = []
        tokens = expression.split()
        precedence_dict = {}

        for associativity, *ops in self.precedence:
            for op in ops:
                precedence_dict[op] = (associativity, len(ops))
        for token in tokens:
            if token.isdigit():
                postfix.append(token)
            else:
                while operator_stack and precedence_dict.get(operator_stack[-1], 0) >= precedence_dict.get(token, 0):
                    postfix.append(operator_stack.pop())
                operator_stack.append(token)
        
        postfix.extend(reversed(operator_stack))
        postfix_str = ' '.join(postfix)

        return postfix_str
