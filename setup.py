from setuptools import find_packages, setup
from typing import List

Hypen_E_DOT = "-e ."
def get_requirements(file_path:str)->List[str]:
    '''
    this function is return list of function
    '''
    
    requirements=[]
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","")for req in requirements]
        
        for Hypen_E_DOT in requirements:
            requirements.remove(Hypen_E_DOT)
    return requirements
        
        

setup(
    name="machine_learning_project_testing",
    version="0.0.1",
    author="Ram",
    author_email="rammahto645@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements("requirements.txt")
    
)