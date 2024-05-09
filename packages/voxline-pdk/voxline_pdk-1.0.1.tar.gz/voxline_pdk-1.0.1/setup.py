from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()

setup (
        name='voxline-pdk',
        version='1.0.1',
        description='sdk to connect with voxline',
        author='inndico',
        license='MIT',
        zip_safe=False,
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=find_packages('src'),
        package_dir={'': 'src'},
)
