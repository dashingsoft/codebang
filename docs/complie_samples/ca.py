from subprocess import Popen, PIPE, STDOUT, TimeoutExpired

import util


def gcc(code: str) -> str:
    filename = util.write2file(code, '.c')

    cmd = ['gcc', '-g',
           '-fdiagnostics-format=json',
           '-fdiagnostics-parseable-fixits',
           '-Werror=implicit-function-declaration',
           filename,
           '-o', filename + '.out',
           ]
    proc = Popen(" ".join(cmd), stdout=PIPE, stderr=STDOUT, shell=True)
    try:
        outs, errs = proc.communicate(timeout=30)
    except TimeoutExpired:
        proc.kill()
        proc.communicate()
        outs = 'The task is killed because of timeout'
    return outs
