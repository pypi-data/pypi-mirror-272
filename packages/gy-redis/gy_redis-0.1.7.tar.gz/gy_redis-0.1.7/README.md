# gy-redis

## pip package
```
pip install gy-redis -U
```

## build package
First change the version or related information of setup.py
```
python setup.py sdist bdist_wheel 
```

## push pypitest
```
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

## push pypi
```
python -m twine upload dist/*
```