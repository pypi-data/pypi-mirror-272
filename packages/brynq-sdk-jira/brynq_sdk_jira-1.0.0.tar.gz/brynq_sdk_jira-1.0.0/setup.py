from setuptools import setup


setup(
    name='brynq_sdk_jira',
    version='1.0.0',
    description='JIRA wrapper from BrynQ',
    long_description='JIRA wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.jira"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'pandas>=1,<3',
        'requests>=2,<=3'
    ],
    zip_safe=False,
)