SETTINGS_PYTHON = '''[tool.mypy]
ignore_missing_imports = true
check_untyped_defs = true

[tool.isort]
profile = "black"
line_length = 79

[tool.ruff]
line-length = 79
indent-width = 4

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F403", "F401"]
"tests/*" = ["F401", "F811"]

[tool.pytest.ini_options]
pythonpath = "."
python_files = "test.py tests.py test_*.py tests_*.py *_test.py *_tests.py"

[tool.taskipy.tasks]
ruff = "ruff check ."
blue = "blue --check . --diff"
isort = "isort --check --diff ."
mypy = "mypy -p <YOUR-PROJECT>"
radon = "radon cc ./<YOUR-PROJECT> -a -na"
bandit = "bandit -r ./<YOUR-PROJECT>"
pydocstyle = "pydocstyle ./<YOUR-PROJECT> --count --convention=google --add-ignore=D100,D104,D105,D107"
lint = "task ruff && task blue && task isort"
format = 'blue .  && isort .'
quality = "task mypy && task radon && task pydocstyle"
pre_test = "task lint"
test = "pytest -s -x --cov=<YOUR-PROJECT> -vv"
post_test = "coverage html"
export-requirements = "rm requirements.txt && poetry export -f requirements.txt --output requirements.txt --without-hashes"
ready = "task lint && task quality && task bandit && pytest -s -x --cov=<YOUR-PROJECT> -vv && task export-requirements"\n\n'''
