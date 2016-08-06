import jinja2
import re


jin_env = jinja2.Environment(loader=jinja2.PackageLoader('generator', '.'), autoescape=False)


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
