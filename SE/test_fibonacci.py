import unittest

#1, 1, 2, 3, 5, 8, 13, 21, 34, ...
#fibo(1) -> 1
#fibo(2) -> 1
#fibo(5) -> 5 
#fibo(8) -> 34


def fibo(n):
	if n == 1: return 1 
	if n == 2: return 1 
	return fibo(n-1) + fibo(n-2)
	

class TestFiboFunction(unittest.TestCase):

    
    def test_1(self):
        self.assertEqual(fibo(1), 1)
    def test_2(self):
        self.assertEqual(fibo(2), 1)
    def test_3(self):
        self.assertEqual(fibo(3), 2)
    def test_4(self):
        self.assertEqual(fibo(6), 8)
    def test_5(self):
        self.assertEqual(fibo(9), 34)
    
    
        


if __name__ == '__main__':
    unittest.main()
