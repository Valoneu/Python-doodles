def lists(a, b, c, d):
    first_list = list(range(a+1))
    second_list = [i+10 for i in first_list]
    second_list[-1] = "KSI"
    if b in second_list:
        second_list.remove(b)
    else:
        print("Not here")
    third_list = first_list[:c]
    second_list.extend(third_list)
    third_list.reverse()
    first_list[1] = d
    first_list.sort()
    return (first_list, second_list, third_list)

print(lists(5, 12, 3, 20))
    # ([0, 2, 3, 4, 5, 20], [10, 11, 13, 14, 'KSI', 0, 1, 2], [2, 1, 0])
print(lists(10, 3, 2, 11))
    # Not here
    # ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 'KSI', 0, 1], [1, 0])

