# OTP Generator
Generate a time-based OTP using SHA-256 hashing algorithm. 

### Installation
You can install the package using pip:
```shell
pip install ownotp
```

### Usage
Create 6 digits otp. OTP will change 2 minutes once based on `your_own_secrent`.
```python
from ownotp.otp import generate_otp

otp = generate_otp('your_own_secret')
print(otp)
```
To change interval time pass the value in seconds.
```python
from ownotp.otp import generate_otp
otp = generate_otp('your_own_secret', interval=120)
```
To get 7 or 8 length otp.
```python
from ownotp.otp import generate_otp
otp = generate_otp('your_own_secret', length=7)
```
To get hashed OTP. Mixed of char and numbers
```python
from ownotp.otp import generate_otp
otp = generate_otp('your_own_secret', only_digits=False)
```