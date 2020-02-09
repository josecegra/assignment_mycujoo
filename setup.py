from setuptools import setup

setup(
    name='assignment_mycujoo',
    version='0.0.1',
    author='Jose Eduardo Cejudo',
    author_email='josecegra@gmail.com',
    packages=['src'],
    include_package_data=True,
    install_requires=[
        "opencv-python==4.2.0.32",
        "pytesseract==0.3.2"

    ],
    entry_points={'console_scripts': ['run_assignment_mycujoo=src.main:main']})


 

