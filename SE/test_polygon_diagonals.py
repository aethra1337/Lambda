import unittest

def get_diagonals(n):

    if n < 3:
        return 0
    
    result = (n * (n - 3)) // 2
    return result

class TestDiagonalCalculation(unittest.TestCase):
    
    def test_triangle(self):
        self.assertEqual(get_diagonals(3), 0)

    def test_square(self):
        self.assertEqual(get_diagonals(4), 2)

    def test_pentagon(self):
        self.assertEqual(get_diagonals(5), 5)

    def test_hexagon(self):
        self.assertEqual(get_diagonals(6), 9)

    def test_decagon(self):
        self.assertEqual(get_diagonals(10), 35)

if __name__ == '__main__':
    unittest.main()