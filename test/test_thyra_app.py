import unittest

class TestThyraApp(unittest.TestCase):

    def test_toggle_thyra(self):
        # Set thyra_running to True before running the test
        selfthyra_running = True
        self.assertTrue(selfthyra_running)


if __name__ == '__main__':
    unittest.main()
