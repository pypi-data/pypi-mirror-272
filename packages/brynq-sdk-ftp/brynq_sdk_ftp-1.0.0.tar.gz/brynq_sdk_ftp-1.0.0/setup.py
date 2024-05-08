from setuptools import setup


setup(
    name='brynq_sdk_ftp',
    version='1.0.0',
    description='FTP wrapper from BrynQ',
    long_description='FTP wrapper from Brynq',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.ftp"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'requests>=2,<=3',
        'paramiko>=2,<=4',
        'pysftp>0.2,<1',
        'tenacity>=8,<9'
    ],
    zip_safe=False,
)