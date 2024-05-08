This is readme
python -m venv venv
venv\Scripts\activate
__init__.py required
pip install setuptools

python setup.py sdist

pip install twine
twine upload dist/*