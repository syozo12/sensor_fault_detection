from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path  ) -> List[str]:
    re=[]
    with open(file_path) as f:
        r=f.readlines()
        for i in r:
            req = i.strip()
            if req and req != "-e .":
                re.append(req)
       
    return re
setup(
    name="fault_detection",
    author="radha",
    version="5.0.0",
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages()
    
)