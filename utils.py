

def char_match_amount(a: str, b: str) -> int|bool:
    match_amount: int = 0
    for index in range(min(len(a), len(b))):
        if a[index] == b[index]:
            match_amount += 1
        else:
            return match_amount
    return index+1



def infinite_number_generator():
    num = 0
    while True:
        yield num
        num+=1



ng = infinite_number_generator()