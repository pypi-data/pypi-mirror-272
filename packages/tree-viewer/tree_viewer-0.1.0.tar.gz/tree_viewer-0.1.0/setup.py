from setuptools import setup, find_packages

setup(
   name='tree-viewer',
   version='0.1.0',
   packages=find_packages(),
   description="Tree-Viewer is a Python tool for generating customizable visual representations of directory trees, ideal for developers who need to manage and navigate complex project structures. It offers a clear, structured view of directory contents, enhancing project organization and accessibility.",
   long_description=open('README.md', encoding='utf-8').read(),
   long_description_content_type='text/markdown',
   author='Wilian Cirillo',
   author_email='wilian@hey.com',
   url='https://github.com/wiliancirillo/tree-viewer',
   license='MIT',
   classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
   ],
   entry_points={
      'console_scripts': [
         'tree-viewer=tree_viewer.main:main'
      ]
   }
)
