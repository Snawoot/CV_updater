from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='hh_cv_updater',
      version='0.1.0',
      description='Tool which updates your CV on hh.ru every 4 hours',
      url='https://github.com/danilasokolov0103/CV_updater',
      author='Danila Sokolov',
      author_email='danilasokolov0103@gmail.com',
      packages=['hh_cv_updater'],
      python_requires='>=3.5.3',
      setup_requires=[
          'wheel',
      ],
      install_requires=[
          'selenium>=3.141.0',
          'webdriver-manager>=2.5.1',
      ],
      entry_points={
          'console_scripts': [
              'hh-cv-updater=hh_cv_updater.__main__:main',
          ],
      },
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: Public Domain",
          "Operating System :: OS Independent",
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: End Users/Desktop",
          "Natural Language :: English",
          "Topic :: Office/Business",
          "Topic :: Other/Nonlisted Topic",
      ],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=True)
