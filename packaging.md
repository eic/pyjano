# PIP packaging instructions
TL;DR;   

```bash
pip install --upgrade pip
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
python2 setup.py bdist_wheel

python3 -m pip install -r requirements.txt --user

python3 -m twine upload dist/*

```

Full:
```bash
 python3 setup.py sdist bdist_wheel && python2 setup.py bdist_wheel && python3 -m twine upload dist/*
```

in virtual env:
``` 
pip install --upgrade pip
pip install --upgrade setuptools wheel twine

#if bug with setuptools
rm 

python setup.py sdist bdist_wheel

python -m twine upload dist/*
```

PACK AND UPLOAD

```bash
python setup.py sdist bdist_wheel && python -m twine upload dist/*
```

Jefferson Lab certificates
```bash
python -m twine upload --cert ~/JLabCA.cer dist/*

```


A tutorial:
https://packaging.python.org/tutorials/packaging-projects/

ejpm pip: https://pypi.org/project/ejpm/#history

SO question for JLab certificate validation
https://stackoverflow.com/questions/10667960/python-requests-throwing-sslerror/10668173



