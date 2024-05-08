from setuptools import setup, find_packages

setup(
    name='HE_Dataset',
    version='0.2.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={'csulb_mock_student_dataset': ['*.csv']},
    install_requires=[
        'pandas',  # Ensure pandas is installed with your package
    ],
    author='Gurucharan Raju',
    author_email='Gurucharan.Raju-SA@csulb.edu@csulb.edu',
    description='A simple package containing a CSV dataset',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)
