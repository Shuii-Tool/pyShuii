python3 setup.py clean --all

python3 setup.py install

python3 setup.py sdist

python3 -m twine upload --repository pypi dist/*
