from typing import Dict, List, Type

from cga import TokenNode, make_token_list


class CODE_TYPE(object):
    C = 'c'
    C_PLUS = 'c++'
    INFO = ''


class CodeBlock(object):
    
    def __init__(self, type: CODE_TYPE) -> None:
        self._block = []
        self.__type = type
    
    def append(self, line: str):
        assert not line.endswith('\n')
        self._block.append(line)

    @property
    def code(self):
        return '\n'.join(self._block) + '\n'

    def __eq__(self, other):
        if self is other:
            return True

        if self.__type != other._CodeBlock__type:
            return False
        if self.code != other.code:
            return False
        return True


class InfoBlock(CodeBlock):
    __header = [
        {'h2': '##'},
        {'text_line': 'error info'},
        {'code_start': '```'}
    ]
    __footer = [{'code_end': '```'}]

    def __init__(self):
        super().__init__(CODE_TYPE.INFO)

    @property
    def tokens(self):
        tokens = []
        for line in self._block:
            tokens.append({'text_line': line})
        res = []
        res.extend(self.__header)
        res.extend(tokens)
        res.extend(self.__footer)
        return res


def hunt(tokens: List[Dict]) -> List[CodeBlock]:
    aim = False
    block = []
    for token in tokens:
        cur = list(token.keys())[0]
        if cur == 'code_start':
            aim = True
            block.append(CodeBlock(token.get('code_start')[3:]))
            continue
        elif cur == 'code_end':
            aim = False
            continue
        if aim:
            block[-1].append(token.get('text_line'))
    return block


def insert(node: Type[TokenNode], tokens: List[Dict[str, str]]) -> None:
    nodelist = make_token_list(tokens)
    node.next, nodelist[-1].next = nodelist[0], node.next
