import unittest

def power(base, exponent):
    result = base ** exponent
    return result

class TestPowerFunction(unittest.TestCase):
    
    def test_positive(self):
        self.assertEqual(power(3, 2), 9)

    def test_negative_base(self):
        self.assertEqual(power(-3, 2), 9)
        self.assertEqual(power(-3, 3), -27)

    def test_negative_exponent(self):
        self.assertEqual(power(2, -1), 0.5)
        self.assertEqual(power(4, -2), 0.0625)

    def test_zero_cases(self):
        self.assertEqual(power(10, 0), 1)
        self.assertEqual(power(-5, 0), 1)

if __name__ == '__main__':
    unittest.main()