### virtual python3 ENV

1. Create virtual ENV → `python3 -m venv .venv`
2. Activate → `source .venv/bin/activate`
3. Check virt env → `echo $VIRTUAL_ENV` → should be non empty output
4. Deactivate → `deactivate` or reopen terminal session

### Install dependencies

`pip install -r requirements.txt`

### Run tests

- A simple way: `python3 -m unittest discover -s ./tests`

- Or beauti → run this: `pytest ./tests`
- run handy test → `python3 -m tests.handy_test`

### Run GitHub actions

- Tests: 1. manual in web or **automaticaly in pull request**.
- Deploy (publish in pypi.org):
    - Manually: just run
      actions → [Publish 🐍 📦 to PyPI](https://github.com/ModularAIDev/tools-alpaca/actions/workflows/deploy.yml)
    - pub by special commit tag to only 'main' branch:
        1. `git commit -m "your release message"` & `git push`
        2. `git tag vx.x.x`; `x` is the numbers! Follow the pattern: 'v[0-9]+.[0-9]+.[0-9]+'
        3. `git push origin vx.x.x`

**P.S. Do not forget increse release version in [stup.py](./setup.py)**

### Alpacas Python SDK

The pypi.org [start page](https://pypi.org/project/alpaca-py/).

Oficial Alpacas [documentation about alpaca-py](https://alpaca.markets/sdks/python/getting_started.html).

### Alpacas Tradin API

Start learn from [About Trading API](https://docs.alpaca.markets/docs/trading-api)