import datetime
import hashlib

def start(mobile):
    value = (mobile + str(datetime.datetime.now())[0:-11])
    result = hashlib.sha224(value.encode())
    otp = []
    hash = result.hexdigest()
    hash1 = (hash[1:-1])
    chunks, chunk_size = len(hash1), len(hash1) // 6
    hashList = [hash1[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
    for digit in hashList:
        sum = 0
        for var in digit:
            sum = sum + ord(var)
        otp.append(sum % 9)
    generated_otp = ("".join(map(str, otp)))
    print("otp", generated_otp)
