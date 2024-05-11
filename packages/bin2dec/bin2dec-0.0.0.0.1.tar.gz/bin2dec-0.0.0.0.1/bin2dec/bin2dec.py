def Bin2Dec(num):
    nums = 0
    for idx, digit in enumerate(str(num)[::-1]):
        nums += int(digit) * (2 ** idx)
    return int(nums)

def Dec2Bin(num):
    x = int(num)
    nums = ""
    while x > 0:
        nums = str(x % 2) + nums
        x = x // 2
    return int(nums)