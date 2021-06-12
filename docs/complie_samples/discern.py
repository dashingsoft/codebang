import re

from cga import Buffer

TITLE_LEVEL = ['h1', 'h2', 'h3', 'h4', 'h5']


def ll_title(buf: Buffer):
    regex = '^#+ '
    group = re.search(regex, buf.buf_str)
    if group:
        match = group.group(0)
        level = TITLE_LEVEL[len(match) - 2]
        sign = match[:-1]
        return {
            'matched': True,
            'token': level,
            'sign': sign,
            'remain': buf.buf_str[len(match):]
        }
    return {
        'matched': False,
        'remain': buf.buf_str
    }


def ll_text_line(buf: Buffer):
    regex = '.+\n\Z'
    group = re.search(regex, buf.buf_str)
    if group:
        match = group.group(0)
        sign = match[:-1]
        return {
            'matched': True,
            'token': 'text_line',
            'sign': sign,
            'remain': ''
        }
    return {
        'matched': False,
        'remain': buf.buf_str
    }


def ll_code_start(buf: Buffer):
    regex = '^```((c|C)(()|(\+{2})))\n\Z'
    group = re.search(regex, buf.buf_str)
    if group:
        match = group.group(0)
        sign = match[:-1]
        return {
            'matched': True,
            'token': 'code_start',
            'sign': sign,
            'remain': ''
        }
    return {
        'matched': False,
        'remain': buf.buf_str
    }


def ll_code_end(buf: Buffer):
    regex = '^```\n'
    group = re.search(regex, buf.buf_str)
    if group:
        match = group.group(0)
        sign = match[:-1]
        return {
            'matched': True,
            'token': 'code_end',
            'sign': sign,
            'remain': ''
        }
    return {
        'matched': False,
        'remain': buf.buf_str
    }


PRIORITY_QUEUE = [ll_title, ll_code_start, ll_code_end, ll_text_line]


def lexer(buf: Buffer):
    tokens = []
    for f in PRIORITY_QUEUE:
        ll = f(buf)
        buf.buf_str = ll.get('remain')
        if ll.get('matched'):
            tokens.append({ll.get('token'): ll.get('sign')})
    return tokens


def lex(file: str):
    res = []
    with open(file, mode='r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break
            buffer = Buffer(line)
            res.extend(lexer(buffer))
        f.close()
    return res
