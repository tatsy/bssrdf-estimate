import os
import sys
import site
import platform
from setuptools import setup, Extension
from setuptools.command.install import install as inst

print('Installing bssrdf-estimate ...')
print('')
print('Platform: %s' % platform.platform())
print('Python: %d.%d' % (sys.version_info.major, sys.version_info.minor))
print('')

sitepackages = []
sitepackages.extend(site.getsitepackages())
sitepackages.append(site.getusersitepackages())

include_dirs = [os.path.join(d, 'numpy/core/include') for d in sitepackages]
include_dirs.append('submodules/spica/include')

render_module = Extension('bssrdf_estimate.render',
                          sources=['native/bssrdf_render.cc'],
                          language='c++',
                          include_dirs=include_dirs,
                          library_dirs=['build/lib'],
                          runtime_library_dirs=['build/bin', 'build/lib'],
                          libraries=['spica_renderer'],
                          extra_compile_args=['-std=c++11']
                          )
filter_module = Extension('bssrdf_estimate.imfilter',
                          sources=['native/bssrdf_filter.cc'],
                          language='c++',
                          include_dirs=include_dirs,
                          extra_compile_args=['-std=c++11']
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
    ext_modules=[filter_module, render_module],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4'
    ],
    packages=[
        'bssrdf_estimate',
        'bssrdf_estimate.hdr',
        'bssrdf_estimate.tools',
        'bssrdf_estimate.interface',
    ]
)
