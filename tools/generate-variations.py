#!/usr/bin/env python
import itertools

def maybe(e):
    return ['', '-'+e]
def readFile(path):
    try:
        return open(path, 'r').read()
    except:
        return None

def writeFile(path, content):
    tmp = ',,,,'
    with open(tmp, 'w') as f:
        f.write(content)
    if (readFile(tmp) != readFile(path)):
        with open(path, 'w') as f:
            f.write(content)

format = '%s-%s%s%s%s.scss'

gg = ['dark', 'light']
cc = {
    'red': 0, 'yellow': 60,
    'green': 120, 'cyan': 180,
    'blue': 240, 'pink': 300
}
oo1 = maybe('draft')
oo2 = maybe('dense')
oo3 = maybe('tiny')

for g,c,draft,dense,tiny in itertools.product(gg, cc, oo1, oo2, oo3):
    params = (g,c,draft,dense,tiny)
    out = format % params
    print(out)
    content = "\n".join([
        '/* This theme is generated by deck.js-theme-builder. */',
        '/*  https://github.com/twitwi/deck.js-theme-builder  */',
        '/* This is a generated theme with parameters %s */' % (str(params)),
        '@import "reset";',
        '@import "theme-chunks";',
        '',
        '@include font%s();' % (draft if draft else '-exo-2'),
        '@include size(%s);' % ('23px' if tiny else '26px'),
        '@include bullets%s();' % (dense),
        '@include %s-colors(%s);' % (g, cc[c]),
        '@include extras(); '
    ])
    writeFile(out, content)
print('')
