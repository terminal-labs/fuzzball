from distutils.core import setup

pins = []

setup(
  name = 'fuzzball',
  packages = ['fuzzball'],
  version = '0.0.1',
  license='TL',
  author = 'Terminal Labs',
  author_email="solutions@terminallabs.com",
  url = 'https://github.com/terminal-labs/fuzzball',
  download_url = 'https://github.com/terminal-labs/fuzzball/archive/master.zip',
  install_requires=pins + [
    "setuptools",
    "standardmodel@git+https://github.com/terminal-labs/standardmodel.git",   
    "inflation@git+https://github.com/terminal-labs/inflation.git",
  ],
  classifiers=[  # Optional
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
  entry_points="""
      [console_scripts]
      fuzzball=fuzzball.cli:main
   """,
)
