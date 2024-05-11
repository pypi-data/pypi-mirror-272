import os
from shutil import copyfile

doc_root = os.getcwd()
this_script_path = os.path.dirname(__file__)

"""
Copy main.py
"""
copyfile(this_script_path+'/main.py', doc_root+'/main.py')
if not os.path.exists(doc_root+'/config.json'):
    copyfile(this_script_path+'/config.json', doc_root+'/config.json')
if not os.path.exists(doc_root+'/api'):
    os.mkdir(doc_root+'/api')
if not os.path.exists(doc_root+'/api/hello.py'):
    copyfile(this_script_path+'/api/hello.py', doc_root+'/api/hello.py')
    copyfile(this_script_path+'/api/__init__.py', doc_root+'/api/__init__.py')

"""
Requirements
"""
f = open(doc_root+"/requirements.txt", "w")
f.write("cloudframework")
f.close()

"""
app.yaml
"""

appyaml = """service: python-test
runtime: python39
"""

f = open(doc_root+"/app.yaml", "w")
f.write(appyaml)
f.close()
print("The following files have been created: main.py, requirements.txt, app.yaml, api/hello.py")
print("To run locally execute:\npython main.py\n")
print("To deploy in standard environment modify app.yaml and change 'service' attribute and execute:\ngcloud app deploy app.yaml --project={your_project_name}\n")
