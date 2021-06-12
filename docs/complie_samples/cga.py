from typing import List, Dict, Type
from util import dict2ins, link_node
import sys


class LexSta:
    START = 1
    PROCESSING = START << 1
    END = START << 2


class StaGraph(object):

    def __init__(self):
        self.__stat__ = LexSta.START

    def evolve(self, sta):
        next = self.__stat__ << 1 & 7

        if not next:
            next = LexSta.START

        if sta ^ next:
            return False
        else:
            self.__stat__ = next
            return True


class Buffer(object):

    def __init__(self, line: str):
        assert line[-1] == '\n'
        self.__buf_ = line
        self.__nxt_ = 0
        self.__cur_ = 0

    def next(self):
        val = self.__buf_[self.__nxt_]
        self.__cur_ = self.__nxt_
        self.__nxt_ += 1
        return val

    def current(self):
        return self.__buf_[self.__cur_]

    def seek(self, offset):
        return self.__buf_[self.__cur_ + offset]

    def seeks(self, offset):
        if offset > 0:
            return self.__buf_[self.__cur_ + 1: self.__cur_ + 1 + offset]
        elif offset < 0:
            return self.__buf_[self.__cur_ + offset: self.__cur_]
        else:
            return self.current()

    @property
    def buf_str(self) -> str:
        return self.__buf_

    @buf_str.setter
    def buf_str(self, value):
        self.__buf_ = value


class TokenNode(object):

    def __init__(self, data: dict):
        self.__data = data
        self.__next = None

    def get(self, key: str):
        return self.__data.get(key)

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, node):
        self.__next = node

    @property
    def key(self):
        return list(self.__data.keys())[0]

    @property
    def val(self):
        return self.get(self.key)

    def __eq__(self, other):
        if not other:
            return False

        if self is other:
            return True

        if self.key != other.key:
            return False

        if self.val != other.val:
            return False

        if self.next != other.next:
            return False

        return True


@link_node
def make_token_list(tokens: List[Dict[str, str]]) -> List[Type[TokenNode]]:
    nodelist = []
    for token in tokens:
        d = {'data': token}
        nodelist.append(dict2ins(d, TokenNode))
    return nodelist


if __name__ == '__main__':
    i_file_path = sys.argv[0]
    stub_data = '''# h1 text
        ## h2 text
        
        ```c
        int main() {
            printf(a);
            return 0;
        }
        ```
        
        ## errorinfo
        ```
        t1.c: In function ‘main’:
        t1.c:2:5: warning: implicit declaration of function ‘printf’ [-Wimplicit-function-declaration]
            2 |     printf(a);
              |     ^~~~~~
        t1.c:2:5: warning: incompatible implicit declaration of built-in function ‘printf’
        t1.c:1:1: note: include ‘<stdio.h>’ or provide a declaration of ‘printf’
          +++ |+#include <stdio.h>
            1 | int main() {
        t1.c:2:12: error: ‘a’ undeclared (first use in this function)
            2 |     printf(a);
              |            ^
        t1.c:2:12: note: each undeclared identifier is reported only once for each function it appears in
        ```
        
        ## h2 text2
        
        ```c
        int main() {
            printf("hello world");
        }
        ```
        ## errorinfo
        ```
        t2.c: In function ‘main’:
        t2.c:2:5: warning: implicit declaration of function ‘printf’ [-Wimplicit-function-declaration]
            2 |     printf("hello world");
              |     ^~~~~~
        t2.c:2:5: warning: incompatible implicit declaration of built-in function ‘printf’
        t2.c:1:1: note: include ‘<stdio.h>’ or provide a declaration of ‘printf’
          +++ |+#include <stdio.h>
            1 | int main() {
        ```
        '''

    with open(i_file_path, 'w', encoding='utf-8') as f:
        f.write(stub_data)
        f.close()
