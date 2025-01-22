import random

def generate_file(filename):
    with open(filename, 'w') as f:
        for _ in range(500000):
            f.write(f"+ {random.randint(2500, 10000)}\n")
            
        f.write("+\n\n<skipping 3884402 B>\n\n")
        for _ in range(100):
            f.write(f"? {random.randint(3000, 160000)} {random.randint(300000, 499999)}\n")

generate_file("output.txt")