try:
    ls = cls.enum_lines()
except NotImplementedError:
    pass
else:
    result['enums'] = []
    for expr in lines_to_statements(ls):
        expr = squash_spaces(expr).split(' ')
        assert expr[0] == 'extern'
        assert expr[1] == 'const'
        assert expr[2] == cls.mapped_class
        assert len(expr) == 4
        result['enums'].append(expr[3])
