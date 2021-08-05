import unittest
import os
import shutil

from rlohhell.utils.logger import Logger, plot_curve

class TestLogger(unittest.TestCase):

    def test_log(self):
        log_dir = "experiments/newtest/test_log.txt"
        if os.path.exists(log_dir):
            shutil.rmtree(log_dir)
        with Logger(log_dir) as logger:
            logger.log("test text")
            logger.log_performance(1, 1)
            logger.log_performance(2, 2)
            logger.log_performance(3, 3)
            plot_curve(logger.csv_path, logger.fig_path, 'Test aglorithm')

if __name__ == '__main__':
    unittest.main()
