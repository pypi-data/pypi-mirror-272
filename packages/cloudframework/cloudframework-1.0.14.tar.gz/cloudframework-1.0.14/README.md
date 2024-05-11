# appengine-python-core-3.9

CloudFramework for Appengine using python language.

## REQUIREMENTS:

1. Install Python3 (min version 3.11): https://cloud.google.com/python/docs/setup#installing_python
2. Add to your path (change for your version): /usr/local/opt/python@3.11/libexec/bin
3. Verify version

Example for MAC environment
```
# install last library of xcode
xcode-select --install

# Install pyenv to work with different versions of python
brew install pyenv

# Install version 3.12
pyenv install 3.12

echo 'export PATH="/usr/local/opt/python@3.12/libexec/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# verify version
python --version
[Python 3.12.3]

pip --version
[pip 24.0]
```

## Creating you development environment

Create your working directory
```
mkdir your-python-project
cd your-python-project
```

Create a virtual environment. It will create a 'env' folder where your libraries will be stored.
```
python -m venv env
source env/bin/activate
# execute 'deactivate' to exit the virtual environment
```

install cloudframework library
```
pip install cloudframework
```

copy the basic files to start working with your APIs developed in python, remamber change the version of your python version
```
python env/lib/python3.12/site-packages/cloudframework/python-dist/install.py
```

Now you have the following structure of files:
```
 - main.py           (main file to run your project)
 - config.json       (cloudframework config file. Intially empty
 - requirements.txt  (packages required when you deploy)
 - api/hello.py      (example of your first API Hellow world)
```

### Running you development environment
Be sure you have activated your virtual environment: `source env/bin/activate`
```
python main.py
# now you can go to: http://localhost:8080/hello
```
