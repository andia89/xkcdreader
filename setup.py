from setuptools import setup
# you may need setuptools instead of distutils

setup(
    # basic stuff here
    name='xkcdreader',
      version='1.0',
      description='Simple XKCD reader',
      author='Andreas Angerer',
    data_files=[
    ('share/icons/hicolor/48x48/apps', ['data/xkcdreader.svg']),
    ('share/applications', ['data/xkcdreader.desktop'])
  ],
    scripts = [
        'scripts/xkcdreader'
    ]
)
