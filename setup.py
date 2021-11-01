from setuptools import setup, find_packages

setup(
    name='lwabish',
    version='0.7.0',
    description=(
        'Collections of python snippets'),
    long_description=open('README.md').read(),
    author='Lwabish',
    author_email='wubw@pku.edu.cn',
    maintainer='Lwabish',
    license='MIT',
    packages=find_packages(),
    url='https://github.com/lwabish/pypi-lwabish',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        # fixme: 待稳定后整理requirements
        # 'lxml',
        # 'requests',
        # 'urllib3',
        # 'pysocks',
        # 'scipy',
        # 'requests_html',
    ]

)
