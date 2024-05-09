import os
from setuptools import setup, find_packages

path_to_my_project = os.path.dirname(__file__)

install_requires = [
    "PyYAML",
    "python-dotenv",
    'ceotr-git-manager>=1.2.1'
]

packages = find_packages(exclude=['tests'])

setup(name='meta_json_downloader',
      version='0.1.0',
      description="A simple library example to download meta files from the meta_json_files repo",
      author="CEOTR",
      author_email="support@ceotr.ca",
      url="https://gitlab.oceantrack.org/ceotr/practice_lab/meta-json-downloader-example",
      packages=packages,
      include_package_data=True,
      license="GNU General Public License v3 (GPLv3)",
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      install_requires=install_requires,
      zip_safe=True
      )
