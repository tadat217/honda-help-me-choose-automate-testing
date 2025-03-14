# HONDA HELP ME CHOOSE MODULE AUTOMATE TEST

## 1. Install

### Create and run virtule enviroment

```bash
$ python -m venv .venv
$ source .venv/bin/activate # MacOS / Linux
$ .venv/Scripts/activate # Windows
```

### Import package

```bash
$ pip install -r requirements.txt
$ playwright install
```

## 2. Run

### For testing

```bash
$ pytest
```

### Get json data from excel

:warning:__IMPORTANT__ make sure to run all theese script after import new excel file to avoid error!

```bash
$ python excel2json_model.py
$ python excel2json_question.py
$ python question2workflow.py
```
