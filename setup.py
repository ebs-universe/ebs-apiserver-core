import setuptools

_requires = [
    'uvicorn',
    'fastapi',
    'loguru',
    'tendril-utils-core>=0.3.2',
]

setuptools.setup(
    name='ebs-apiserver-core',
    url='',

    author='Chintalagiri Shashank',
    author_email='shashank.chintalagiri@gmail.com',

    description='Core Architecture for the EBS API Server Platform',
    long_description='',

    packages=setuptools.find_packages(),
    package_dir={'ebs.apiserver': 'ebs/apiserver'},
    package_data={'ebs.apiserver': ['resources/*.*']},

    install_requires=_requires,
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
    ],
    entry_points={
          'console_scripts': [
              'apiserver = ebs.apiserver.core.server:run_server'
          ]
    },
)
