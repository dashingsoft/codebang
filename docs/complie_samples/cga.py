import logging
from typing import List, Dict

from util import dict2ins, link_node


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
        logging.info('self  key:' + self.key)
        logging.info('other key:' + other.key)
        logging.info('self  val:' + self.val)
        logging.info('other val:' + other.val)

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

    def __str__(self) -> str:
        return str(self.__data)


@link_node
def make_token_list(tokens: List[Dict[str, str]]) -> List[TokenNode]:
    nodelist = []
    for token in tokens:
        d = {'data': token}
        nodelist.append(dict2ins(d, TokenNode))
    return nodelist
