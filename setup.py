from setuptools import setup, Extension
from setuptools.command.install import install as inst

module = Extension('bssrdf_estimate.render',
                   ['native/bssrdf_render.cc'],
                   include_dirs=['submodules/spica/include', 'C:/Python34/Lib/site-packages/numpy/core/include'],
                   library_dirs=['build/lib'],
                   libraries=['spica_renderer']
                   )

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
    ext_modules=[module],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4'
    ],
    packages=[
        'bssrdf_estimate'
    ]
)
