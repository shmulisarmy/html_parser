def infinite_number_generator():
    num = 0
    while True:
        yield num
        num+=1



ng = infinite_number_generator()