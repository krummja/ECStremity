from setuptools import find_packages, setup
import sys

install_requires=['uuid']
if sys.version_info < (3, 5):
    install_requires.append('typing')


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='ecstremity',
    version='1.0.0',
    author='Jonathan Crum',
    author_email="crumja4@gmail.com",
    url="https://github.com/krummja/ECStremity",
    license='MIT',
    description='An ECS Library based on the JavaScript geotic library.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    packages=find_packages(include=['ecstremity', 'ecstremity.registries']),
    test_suite='tests',
    python_requires='>=3.8.5',
)
