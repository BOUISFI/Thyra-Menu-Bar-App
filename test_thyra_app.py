import unittest

from thyra_app import ThyraApp

class TestThyraApp(unittest.TestCase):

    def setUp(self):
        self.app = ThyraApp()
        self.app.run()

    def test_toggle_thyra(self):
        # Test starting Thyra
        self.app.toggle_thyra()
        self.assertTrue(self.app.thyra_running)
        self.assertEqual(self.app.action3.text(), "Stop Thyra")

        # Test stopping Thyra
        self.app.toggle_thyra()
        self.assertFalse(self.app.thyra_running)
        self.assertEqual(self.app.action3.text(), "Start Thyra")

    def quit(self):
        self.app.quit()

if __name__ == '__main__':
    unittest.main()
