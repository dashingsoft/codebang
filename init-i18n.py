#! /usr/bin/env python3
#
# Search the files list in the command line and print the translated
# messages like
#
#    $t('xxxxx')
#    _t('xxxxx')
#
# Usage:
#
#    python3 init-i18n.py $(find src -name *.vue)
#
import re
import sys


def build_message_table(files):
    messages = {}
    pat = re.compile(r'''[_$]t\(\s*[']([^']+)[']\s*[,)]''')
    for name in files:
        print('Searching %s ...' % name)
        with open(name) as f:
            n = 0
            for line in f:
                n += 1
                for msg in re.findall(pat, line):
                    if msg in messages:
                        messages[msg].append((name, n))
                    else:
                        messages[msg] = [(name, n)]

    indent = ' ' * 4
    result = []
    for msg, locations in messages.items():
        for loc in locations:
            result.append('{0}// {1} {2}'.format(indent, *loc))
        result.append('{0}"{1}": "",'.format(indent, msg))
        result.append('')
    return result


if __name__ == '__main__':
    files = sys.argv[1:]
    # print('Search files: %s' % files)

    result = build_message_table(files)
    print('\n'.join(result))
