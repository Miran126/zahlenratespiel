import unittest
import app

class Testing(unittest.TestCase):

    def test_getHighscore(self):
       self.assertIs(type(app.getHighscore()), type([]))
       self.assertEquals(len(app.getHighscore()), 10)

        
if __name__ == '__main__':
    unittest.main()