from setuptools import setup, find_packages

setup(
    name='luabish',
    version='0.0.6',
    description=(
        'A Luabish\'s self use toolbox:Collections of all types of basic python codes.'),
    long_description=open('README.md').read(),
    author='Luabush Wu',
    author_email='imwubowen@gmail.com',
    maintainer='Luabish Wu',
    license='MIT',
    packages=find_packages(),
    url='https://github.com/luabish/luabish',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'lxml',
        'requests',
        'urllib3',
        'pysocks',
        # 'scipy',
        'requests_html',
    ]

)
