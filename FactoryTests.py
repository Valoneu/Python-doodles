import time

iterations_per_second = 1
sleep_time = 1.0 / iterations_per_second
iteration_number = 0
while True:
    start_time = time.perf_counter()
    
    end_time = time.perf_counter()
    elapsed_time = (end_time - start_time) * 100
    iteration_number += 1
    if(iteration_number % iterations_per_second == 0):
      print(f"Update {iteration_number}: {elapsed_time:.5f} ms")
    time.sleep(sleep_time)
