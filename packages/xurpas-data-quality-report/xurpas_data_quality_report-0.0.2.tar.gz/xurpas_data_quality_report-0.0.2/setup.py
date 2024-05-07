from setuptools import setup, find_packages

setup(
    name='Xurpas Data Quality Report',
    version = '0.0.2',
    packages = find_packages(
        where='src',
        include=['xurpas_data_quality*']),
    package_dir={"":"src"},
    author='Neil Ortaliz',
    author_email='neillaurenceortaliz@gmail.com',
    description='XAIL Data quality',
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib'
    ]
)