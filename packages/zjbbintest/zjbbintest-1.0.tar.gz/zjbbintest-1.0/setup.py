from setuptools import setup, find_packages

setup(
    name='zjbbintest',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'attrs==23.2.0',
        'certifi==2024.2.2',
        'charset-normalizer==3.3.2',
        'idna==3.7',
        'importlib_resources==6.4.0',
        'Jinja2==3.1.4',
        'jsonschema==4.21.1',
        'jsonschema-specifications==2023.12.1',
        'MarkupSafe==2.1.5',
        'pkgutil_resolve_name==1.3.10',
        'referencing==0.34.0',
        'requests==2.31.0',
        'rpds-py==0.18.0',
        'urllib3==2.2.1',
        'zipp==3.18.1',
    ],
)