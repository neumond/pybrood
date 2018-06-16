import pytoml as toml
import enscons
import sys


with open('pyproject.toml') as f:
    metadata = dict(toml.load(f))['tool']['enscons']

full_tag = 'py2.py3-none-any'

env = Environment(
    tools=['default', 'packaging', enscons.generate],
    PACKAGE_METADATA=metadata,
    ROOT_IS_PURELIB=False,
    WHEEL_TAG=full_tag,
)

wheel = env.WhlFile(
    env.Whl(
        'platlib',
        Glob('output/Release/inner.pyd') + Glob('pybrood/**/*.py'),
    )
)

env.Default(wheel)
