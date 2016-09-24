import jinja2
import re
from sys import stderr
from itertools import count
from html import unescape as html_unescape


jin_env = jinja2.Environment(loader=jinja2.PackageLoader('generator', 'templates'), autoescape=False)


def indent_lines(lines, shift=4):
    if isinstance(lines, str):
        lines = lines.split('\n')
    ind = ' ' * shift
    return ''.join(map(lambda x: ind + x + '\n', lines))


def squash_spaces(line):
    return re.sub('\s+', ' ', line)


class flines:
    def __init__(self, fname):
        with open(fname) as f:
            self.lines = tuple(line for line in f)

    def __call__(self, start, end):
        return self.lines[start-1:end]  # 1-based, inclusive


def transform_case(name):
    upse, pos, out = 0, 0, []
    for i, ch in enumerate(name):
        if ch.isupper():
            if upse == 0:
                out.append(name[pos:i].lower())
                pos = i
            upse += 1
        else:
            if upse > 1:
                out.append(name[pos:i - 1].lower())
                pos = i - 1
            upse = 0
    if upse == 0:
        out.append(name[pos:].lower())
    else:
        out.append(name[pos:].lower())
    return '_'.join(filter(lambda x: x, out))


ecount = count(start=1)


def outerr(line):
    n = next(ecount)
    print('{}. {}'.format(n, line), file=stderr)


def render_template(template, **kw):
    return html_unescape(jin_env.get_template(template).render(**kw))
