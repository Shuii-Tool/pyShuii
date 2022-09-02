python3 setup.py install

python3 -m twine upload --repository pypi dist/*

python3 setup.py clean --all