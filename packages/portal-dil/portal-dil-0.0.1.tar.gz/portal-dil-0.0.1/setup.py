from setuptools import setup,find_packages


def readme():
	with open('README.md','r') as f:
		return f.read()


setup(
	name='portal-dil',
	version='0.0.1',
	author='bigi',
	author_email='mark25@inbox.ru',
	description='',
	long_description=readme(),
	long_description_content_type='text/plain',
	url='http://',
	packages=find_packages(),
	install_requires=['requests>=2.25.1'],
	classifiers=[
		'Programming Language :: Python :: 3.10',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent'
	],
	keywords='files portal-dil',
	project_urls={
		'GitHub': 'https://github.com/'
	},
	python_requires='>=3.8'
)