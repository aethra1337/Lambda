import unittest

def is_prime(number):
    if number < 2:
        return False
    
    
    for i in range(2, number):
        if number % i == 0:
            return False
            
    return True

class TestPrime(unittest.TestCase):
    
    def test_prime_seven(self):
        self.assertEqual(is_prime(7), True)

    def test_prime_ten(self):
        self.assertEqual(is_prime(11), True)

    def test_prime_two(self):
        self.assertEqual(is_prime(2), True)

    def test_prime_one(self):
        self.assertEqual(is_prime(1), False)

if __name__ == '__main__':
    unittest.main()