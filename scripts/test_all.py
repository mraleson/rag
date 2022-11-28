#!/usr/bin/env python3

import os
from subprocess import call

base = os.path.abspath(os.path.dirname(__file__))

print("Running integration tests...")

print("== Running Rag Unit Tests ==")
# call('poetry run poe test', shell=True)

# micro
print("== Running Micro Template Tests ==")
path = os.path.join(base, '../rag/templates/micro')
result = call(f'cd {path} && rag test', shell=True)
assert result == 0, "Testing micro template failed"

# small
print("== Running Small Template Tests ==")
path = os.path.join(base, '../rag/templates/small')
result = call(f'cd {path} && rag test', shell=True)
assert result == 0, "Testing small template failed"

print("== Testing Small Template Migrations ==")
path = os.path.join(base, '../rag/templates/small')
call(f'cd {path} && rm testing.sqlite3', shell=True)
result = call(f'cd {path} && export RAG_ENV=testing && rag manage migrate api', shell=True)
assert result == 0, "Testing small migrations failed"

# medium
print("== Running Medium Template Tests ==")
path = os.path.join(base, '../rag/templates/medium')
result = call(f'cd {path} && rag test', shell=True)
assert result == 0, "Testing medium template failed"

print("== Testing Medium Template Migrations ==")
path = os.path.join(base, '../rag/templates/medium')
call(f'cd {path} && rm testing.sqlite3', shell=True)
result = call(f'cd {path} && export RAG_ENV=testing && rag manage migrate api', shell=True)
assert result == 0, "Testing medium migrations failed"

# large
print("== Running Large Template Tests ==")
path = os.path.join(base, '../rag/templates/large')
result = call(f'cd {path} && rag test', shell=True)
assert result == 0, "Testing large template failed"

print("== Testing Large Template Migrations ==")
path = os.path.join(base, '../rag/templates/large')
call(f'cd {path} && rm testing.sqlite3', shell=True)
result = call(f'cd {path} && export RAG_ENV=testing && rag manage migrate api', shell=True)
assert result == 0, "Testing large migrations failed"
