from setuptools import setup

setup(
    name='buildbot_pipeline',
    version='0.11.2',
    url='https://github.com/baverman/buildbot_pipeline/',
    license='MIT',
    author='Anton Bobrov',
    author_email='baverman@gmail.com',
    description='Pipeline syntax for buildbot',
    long_description=open('README.rst', 'rb').read().decode('utf-8'),
    long_description_content_type='text/x-rst',
    packages=['buildbot_pipeline', 'buildbot_pipeline.web'],
    package_data={
        '': ['web/dist/*', 'web/dist/assets/*']
    },
    install_requires=['covador'],
    entry_points='''
        [buildbot.www]
        file-store = buildbot_pipeline.file_store:ep
        bb-pipeline = buildbot_pipeline.web:ep
    ''',
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
