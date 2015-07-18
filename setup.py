from setuptools import setup
from setuptools.command.install import install as inst

class install(inst):
    def run(self):
        super(install, self).run()

setup(
    cmdclass = {'install': install},
    name='bssrdf_estimate',
    version='0.1',
    author='tatsy',
    author_email='tatsy.mail@gmail.com',
    url='https://github.com/tatsy/bssrdf-estimate.git',
    description='Implementation of "BSSRDF Estimation from Single Images by Munoz et al. (Eurographics 2011)"',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4'
    ],
    packages=[
        'bssrdf_estimate'
    ]
)
