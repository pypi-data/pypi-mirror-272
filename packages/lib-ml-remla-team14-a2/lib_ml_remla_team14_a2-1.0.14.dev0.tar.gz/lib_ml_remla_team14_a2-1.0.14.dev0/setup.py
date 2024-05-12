
from setuptools import setup, find_packages
import os
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lib_ml_remla_team14_a2',
    use_scm_version={"local_scheme": "no-local-version"
                     },
    setup_requires=['setuptools_scm'],
    author='Yang Li',
    author_email='ly20000325@gmail.com',
    description='A ML preprocessing library.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/07Liyang/lib_ml',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'tensorflow'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)
