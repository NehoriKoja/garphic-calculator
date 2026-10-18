import math
import re

def split_the_string(math_problem):
    pattern = r"3√|√|\d+(?:\.\d+)?|[()+\-*/^]"
    tokens = []
    position = 0

    # Tokenize and reject invalid characters
    for match in re.finditer(pattern, math_problem):
        if math_problem[position:match.start()].strip():
            raise ValueError("Invalid character in expression")

        tokens.append(match.group())
        position = match.end()

    if math_problem[position:].strip():
        raise ValueError("Invalid character in expression")

    # Add implicit multiplication
    result = []

    for token in tokens:
        if result:
            previous = result[-1]

            previous_ends_value = (
                re.fullmatch(r"\d+(?:\.\d+)?", previous) is not None
                or previous == ")"
            )

            current_starts_value = token in ("√", "3√", "(")

            if previous_ends_value and current_starts_value:
                result.append("*")

        result.append(token)

    return result


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def parse_to_tree(tokens):
    precedence = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "u+": 3,
        "u-": 3,
        "^": 4,
        "√": 5,
        "3√": 5
    }

    output = []
    operators = []
    right_associative = {"^", "u-", "u+"}

    def apply_operator(op):
        if op in ("u-", "u+", "√", "3√"):
            if not output:
                raise ValueError(f"Missing operand for {op}")

            right = output.pop()
            output.append(Node(op, None, right))
        else:
            if len(output) < 2:
                raise ValueError(f"Missing operand for {op}")

            right = output.pop()
            left = output.pop()
            output.append(Node(op, left, right))

    previous_token = None

    for token in tokens:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            output.append(Node(token))

        elif token == "(":
            operators.append(token)

        elif token == ")":
            while operators and operators[-1] != "(":
                apply_operator(operators.pop())

            if not operators:
                raise ValueError("Mismatched parentheses")

            operators.pop()

            if operators and operators[-1] in ("√", "3√"):
                apply_operator(operators.pop())

        elif token in ("√", "3√"):
            operators.append(token)

        elif token in ("+", "-") and (
            previous_token is None
            or previous_token in (
                "+", "-", "*", "/", "^", "(", "√", "3√"
            )
        ):
            # Unary plus/minus
            operators.append("u+" if token == "+" else "u-")

        elif token in precedence:
            while (
                operators
                and operators[-1] != "("
                and operators[-1] in precedence
                and (
                    precedence[operators[-1]] > precedence[token]
                    or (
                        precedence[operators[-1]] == precedence[token]
                        and token not in right_associative
                    )
                )
            ):
                apply_operator(operators.pop())

            operators.append(token)

        else:
            raise ValueError(f"Unknown token: {token}")

        previous_token = token

    while operators:
        op = operators.pop()

        if op == "(":
            raise ValueError("Mismatched parentheses")

        apply_operator(op)

    if len(output) != 1:
        raise ValueError("Invalid expression")

    return output[0]


def evaluate_tree(node):
    if node is None:
        raise ValueError("Empty expression")

    # Number
    if node.left is None and node.right is None:
        return float(node.value)

    # Unary operators
    if node.left is None:
        value = evaluate_tree(node.right)

        if node.value == "u-":
            return -value

        if node.value == "u+":
            return value

        if node.value == "√":
            if value < 0:
                raise ValueError(
                    "Cannot calculate real square root of a negative number"
                )
            return math.sqrt(value)

        if node.value == "3√":
            if value < 0:
                return -((-value) ** (1 / 3))
            return value ** (1 / 3)

        raise ValueError(f"Unknown unary operator: {node.value}")

    # Binary operators
    left_val = evaluate_tree(node.left)
    right_val = evaluate_tree(node.right)

    if node.value == "+":
        return left_val + right_val

    if node.value == "-":
        return left_val - right_val

    if node.value == "*":
        return left_val * right_val

    if node.value == "/":
        return left_val / right_val

    if node.value == "^":
        return left_val ** right_val

    raise ValueError(f"Unknown operator: {node.value}")

def Calc(p):
    tokens = split_the_string(p)
    root_node = parse_to_tree(tokens)
    return str(evaluate_tree(root_node))