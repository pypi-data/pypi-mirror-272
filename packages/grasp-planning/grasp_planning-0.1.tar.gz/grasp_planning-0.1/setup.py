import setuptools
import os

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"
install_requires = [] # Here we'll add: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setuptools.setup(
    name="grasp_planning", 
    version  = '0.1',
    author="Tomas Merva", 
    author_email='tmerva7@gmail.com',
    description='Grasp and Motion Planning Python Package',
    long_description='Grasp and Motion Planning Python Package',
    install_requires=install_requires
)