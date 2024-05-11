from distutils.core import setup
setup(
  name = 'gtestsPackage',         # How you named your package folder (MyLib)
  packages = ['gtests'],   # Chose the same as "name"
  version = '0.0.8',      # Start with a small number and increase it with every change you make
  license='GPL-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Graph-Based Two Sample Test',   # Give a short description about your library
  author = 'Alexander Wold',                   # Type in your name
  author_email = 'alexwold@iastate.edu',      # Type in your E-Mail
  url = 'https://github.com/atwold/gtests.git',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/atwold/gtests/archive/refs/tags/0.0.4.tar.gz',    # I explain this later on
  keywords = ['TWO-SAMPLE', 'GRAPH-BASED', 'GRAPH', 'TWO SAMPLE', 'GRAPH BASED', 'TEST', 'NONPARAMETRIC'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'scipy',
          'ctypes',
          'os',
          'sklearn',
          'matplotlib'
      ],
  classifiers=[
    'Development Status :: 3 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: ',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: GNU Affero General Public License v3',   # Again, pick a license

    'Programming Language :: Python :: 3'      #Specify which pyhton versions that you want to support
  ],
)
