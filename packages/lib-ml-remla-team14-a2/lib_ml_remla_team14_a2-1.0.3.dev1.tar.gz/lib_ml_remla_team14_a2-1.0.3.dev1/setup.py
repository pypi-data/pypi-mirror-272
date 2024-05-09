
from setuptools import setup, find_packages

setup(
    name='lib_ml_remla_team14_a2',
    use_scm_version={'root': '.', 'relative_to': __file__, 'write_to': 'lib_ml/version.py',
                     "local_scheme": "no-local-version"},
    setup_requires=['setuptools_scm'],
    author='Yang Li',
    author_email='ly20000325@gmail.com',
    description='A ML preprocessing library.',
    long_description=open('README.md').read(),
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
