import unittest

def power(base, exponent):
    result = base ** exponent
    return result

class TestPowerFunction(unittest.TestCase):
    
    def test1(self):
        self.assertEqual(power(3, 2), 9)

    def test2(self):
        self.assertEqual(power(6, 2), 36)

    def test3(self):
        self.assertEqual(power(10, 0), 1)

    def test4(self):
        self.assertEqual(power(7, 1), 7)

if __name__ == '__main__':
    unittest.main()