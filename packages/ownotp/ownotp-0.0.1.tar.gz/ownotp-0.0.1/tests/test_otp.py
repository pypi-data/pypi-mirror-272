import time
import unittest
from src.otp import generate_otp


class TestOTP(unittest.TestCase):
    def test_generate_otp(self):
        otp_one = generate_otp('9865321470')
        time.sleep(15)
        otp_two = generate_otp('9865321470')
        self.assertEqual(otp_one, otp_two)


if __name__ == '__main__':
    unittest.main()
