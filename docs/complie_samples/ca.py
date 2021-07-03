from subprocess import Popen, PIPE, STDOUT, TimeoutExpired

import util
from cga import TokenNode
from parser import InfoBlock, CodeBlock


def gcc(code: str) -> str:
    filename = util.write2file(code, '.c')

    cmd = ['gcc', '-g',
           # '-fdiagnostics-format=json',
           '-fdiagnostics-parseable-fixits',
           '-Werror=implicit-function-declaration',
           filename,
           '-o', filename + '.out',
           ]
    proc = Popen(" ".join(cmd), stdout=PIPE, stderr=STDOUT, shell=True)
    try:
        outs, errs = proc.communicate(timeout=30)
        assert isinstance(outs, bytes)
        outs = outs.decode('utf-8')
    except TimeoutExpired:
        proc.kill()
        proc.communicate()
        outs = 'The task is killed because of timeout'
    return outs


def build_block(error_info: str, block_type=InfoBlock) -> CodeBlock:
    assert isinstance(error_info, str)
    block = block_type()
    for line in error_info.split('\n'):
        block.append(TokenNode({'text_line': line}))
    return block
