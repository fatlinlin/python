from distutils.core import setup

setup(
    name='Efront',
    version='0.1.0',
    author='Simon Bergot',
    author_email='sbergot@efront.com',
    packages=['efront', 'efront.test'],
    scripts=['bin/genCode.py',
             'bin/switch.py',
             'bin/merge.py',
             'bin/merge.json',
             'bin/current.py',
             'bin/dev.py'],
    license='LICENSE.txt',
    description='useful env tools',
    long_description=open('README.md').read(),
)
