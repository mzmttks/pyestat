from setuptools import setup
import sys

sys.path.append('./pyestat')
sys.path.append('./test')

setup(name="pyestat",
      version="0.1",
      description="Python interface of e-Stat",
      test_suite='test_getData.suite'
)
