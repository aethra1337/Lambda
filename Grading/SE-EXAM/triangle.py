import unittest

# the formula for the triangle condition
def check_triangle(a, b, c):
    # sides must be > 0 
    if a <= 0 or b <= 0 or c <= 0:
        return False
        
    # triangle inequality theorem check
    if (a + b > c) and (a + c > b) and (b + c > a):
        return True
    
    return False


# function unittesting
class TestTriangleFunction(unittest.TestCase):
    
    def test_valid_triangles(self):
        self.assertTrue(check_triangle(3, 4, 5))
        self.assertTrue(check_triangle(5, 5, 5)) # equilateral triangle test (a type of triangle with two sides of equal length and one side of a different length)
        
    def test_invalid_triangles(self):
        # structures that are not suitable for forming a triangle
        self.assertFalse(check_triangle(1, 2, 3))
        self.assertFalse(check_triangle(10, 2, 2))
        
    def test_invalid_inputs(self):
        # testing zero and negative numbers (these cannot be triangles)
        self.assertFalse(check_triangle(0, 5, 5))
        self.assertFalse(check_triangle(-3, 4, 5))

if __name__ == '__main__':
    unittest.main()