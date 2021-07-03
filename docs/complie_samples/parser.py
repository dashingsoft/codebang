from typing import Dict, List, Type

from cga import TokenNode, make_token_list


class CODE_TYPE(object):
    C = 'c'
    C_PLUS = 'c++'
    INFO = ''


class CodeBlock(object):

    def __init__(self, type: CODE_TYPE) -> None:
        self._block: List[TokenNode] = []
        self.__type = type

    def append(self, node: TokenNode):
        if len(self._block):
            self.end.next = node
        self._block.append(node)

    def token_keys(self):
        for i in self._block:
            yield i.key

    def token_values(self):
        for i in self._block:
            yield i.val

    @property
    def code(self):
        return '\n'.join(list(self.token_values())[1:-1]) + '\n'

    @property
    def head(self):
        return self._block[0]

    @property
    def end(self):
        return self._block[-1]

    def __eq__(self, other):
        if self is other:
            return True

        if self.__type != other._CodeBlock__type:
            return False
        if self.code != other.code:
            return False
        return True

    def __str__(self) -> str:
        return self.code


class InfoBlock(CodeBlock):
    __header = [
        {'text_line': ''},
        {'h2': '##'},
        {'text_line': 'error info'},
        {'code_start': '```'}
    ]
    __footer = [
        {'code_end': '```'},
        {'text_line': ''}
    ]

    def __init__(self):
        super().__init__(CODE_TYPE.INFO)

    def __str__(self):
        return str(self.tokens)

    @property
    def tokens(self):
        tokens = []
        tokens.extend(self.__header)
        for node in self._block:
            tokens.append({'text_line': node.val})
        tokens.extend(self.__footer)
        return tokens


def hunt(nodes: List[TokenNode]) -> List[CodeBlock]:
    aim = False
    block = []
    for node in nodes:
        cur = node.key
        if cur == 'code_start':
            aim = True
            block.append(CodeBlock(node.val[3:]))
        if aim:
            block[-1].append(node)
        if cur == 'code_end':
            aim = False
    return block


def insert_tokens(node: TokenNode, tokens: List[Dict[str, str]]) -> None:
    nodes_for_inserting = make_token_list(tokens)
    node.next, nodes_for_inserting[-1].next = nodes_for_inserting[0], node.next


def insert(node: TokenNode, block: InfoBlock) -> None:
    insert_tokens(node, block.tokens)
