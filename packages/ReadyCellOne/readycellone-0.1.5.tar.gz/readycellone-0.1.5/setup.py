from setuptools import setup

setup(name='ReadyCellOne',
      version='0.1.5',
      description='Computational tools to enable task-centric cell engineering',
      url='http://github.com/CahanLab/ReadyCellOne/',
      author='Patrick Cahan',
      author_email='patrick.cahan@gmail.com',
      license='MIT',
      packages=['ReadyCellOne'],
      install_requires=[
          'scanpy',
          'gseapy',
          'harmonypy',
          'scikit-learn',
          'matplotlib',
          'seaborn'
      ],
      zip_safe=False)