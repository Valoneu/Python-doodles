def collatz(n):
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n /= 2
        else:
            n = n * 3 + 1
        sequence.append(n)
    return sequence

for i in range(1, 1000):
    print(f"Starting from {i}:")
    print(collatz(i))