from setuptools import setup, find_packages

setup(
    name='zzd-cli',
    version='0.3.0',
    packages=find_packages(),
    include_package_data=True,
    author='messizqin', 
    author_email='1021358459@qq.com',
    description='走之底科技zzd.show客户端cli',
    install_requires=[
        'click',
        'requests',
        'chardet', 
        'urllib3==1.26.16', 
        'beautifulsoup4', 
    ],
    entry_points='''
        [console_scripts]
        zzd=zzd.cli:zzd
    ''',
)