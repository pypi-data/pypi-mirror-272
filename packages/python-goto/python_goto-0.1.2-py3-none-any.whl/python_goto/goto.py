# Imports:
from inspect import getsourcelines
from sys import modules

# Typing:
from types import ModuleType

def goto(line: int) -> None:
    module: ModuleType = modules['__main__']
    source_lines, _ = getsourcelines(modules['__main__'])
    if line >= 0 and line < len(source_lines):
        source_code: str = '\n'.join(source_lines[line - 1:])
        exec(source_code, module.__dict__)
    else:
        error: str = f'{line} is out of range ({1}, {len(source_lines) + 1})'
        raise Exception(error)