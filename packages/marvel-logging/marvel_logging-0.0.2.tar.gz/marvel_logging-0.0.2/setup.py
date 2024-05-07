from setuptools import setup, find_packages
setup(
	name='marvel_logging',
	version='0.0.2',
	author='',
	author_email='',
	description='',
	url='https://github.azc.ext.hp.com/co-mlops-platform/marvel',
	license='HP Internal Use Only',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True
)