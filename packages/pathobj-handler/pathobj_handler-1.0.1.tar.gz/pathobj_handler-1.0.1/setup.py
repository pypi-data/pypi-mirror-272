from setuptools import find_packages, setup

setup(
    name='pathobj_handler',
    version='1.0.1',
    description='',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/toritamantaro/path-object-handler',
    author='toritamantaro',
    packages=(
        find_packages(
            include=['pathobj_handler', 'pathobj_handler.filestem'],
            exclude=['resource']
        )
    ),
    python_requires='>=3.9',
    license='MIT',
    install_requires=[
        'python-dateutil',
    ],
)
