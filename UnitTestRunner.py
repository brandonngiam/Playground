# https://stackoverflow.com/questions/3295386/python-unittest-and-discovery
# Run this 'python UnitTestRunner.py' to run all unittests
import unittest
start_dir_list = ['./']
for start_dir in start_dir_list:
    print(f'Folder: {start_dir}')
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir, pattern='Test*.py')
    runner = unittest.TextTestRunner()
    runner.run(suite)