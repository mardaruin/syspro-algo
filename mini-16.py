def infix_to_postfix(expression):
    operators_with_priority = {
        '(' : 0,
        '+' : 1, '-' : 1,
        '*' : 2, '/' : 2,
        '^' : 3,
        '<' : 4, '>' : 4, '<=': 4, '>=': 4, '==': 4, '!=': 4,
        '&' : 5, '|' : 6, '~' : 12, '<<' : 8, '>>' : 9,
        '&&' : 10, '||' : 11, '!' : 12
    }

    right_associative = {'^', '~', '!'}

    output = []
    stack = []

    tokens = expression.split()

    for token in tokens:
        if token.isdigit() or token.isalpha():
            output.append(token)
            while stack and (stack[-1] == '~' or stack[-1] == '!'):
                output.append(stack.pop())
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()
        elif token in operators_with_priority:
            while stack and stack[-1] != '(' and ((token in right_associative and operators_with_priority[stack[-1]] > operators_with_priority[token]) or (token not in right_associative and operators_with_priority[stack[-1]] >= operators_with_priority[token])):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return ' '.join(output)

expression = "( ( a + b ) * ( c - d ) ) + ( ( e * f ) / g )"
assert(infix_to_postfix(expression) == "a b + c d - * e f * g / +")

expression = "- a + ( - b ) * c"
assert(infix_to_postfix(expression) == "a - b - c * +")

expression = "~ a && ! b || c ^ d"
assert(infix_to_postfix(expression) == "a ~ b ! c || && d ^")

expression = "a ^ b ^ c"
assert(infix_to_postfix(expression) == "a b c ^ ^")

