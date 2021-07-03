import logging
import subprocess
from time import time
import os
from typing import TypeVar
import inspect

logging.basicConfig(level=logging.INFO)


def write2file(text: str, ext='.md') -> str:
    t_dir = 'build'
    target = str(int(time())) + ext
    if not os.path.exists(t_dir):
        os.mkdir(t_dir)
    file_path = t_dir + '/' + target
    with open(file_path, mode='w', encoding='utf-8') as tf:
        tf.write(text)
        tf.close()
    return file_path


def execute_in_sys(cmd: str) -> None:
    logging.info(cmd)
    os.system(cmd)


def execute_in_shell(cmd: list) -> str:
    logging.info(cmd)
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    logging.info(res.stdout)
    return res.stdout


T = TypeVar('AnyClass')


def dict2ins(d: dict, cls: T) -> T:
    if inspect.isclass(cls):
        constructor = getattr(cls, '__init__')
        params = inspect.signature(constructor).parameters
        values = []
        for name, param in params.items():
            if d.get(name):
                values.append(d.get(name))

        return cls(*values)
    else:
        raise ValueError('the argument "cls" must be a class')


def link_node(func):
    def link(tokens):
        nodelist = func(tokens)
        for i in range(len(nodelist) - 1):
            nodelist[i].next = nodelist[i + 1]
        return nodelist
    return link
