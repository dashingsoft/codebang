from typing import List

import discern
from cga import TokenNode


def convert_to_inlines(nodelist: List[TokenNode]) -> List[str]:
    inlines = []
    node = nodelist[0]
    while node:
        if node.key in discern.TITLE_LEVEL:
            inlines.append(node.val + ' ' + node.next.val)
            node = node.next.next
            continue
        inlines.append(node.val)
        node = node.next
    return inlines


def write_to_md(nodelist: List[TokenNode], target: str) -> None:
    inlines = convert_to_inlines(nodelist)
    with open(target, mode='w', encoding='utf-8') as f:
        for line in inlines:
            f.write(line + '\n')
        f.close()
