
def longest_common_substring(str1, str2):

    matrix_row = [0] * len(str2)

    max_value = 0
    max_value_row = 0

    for row in range(len(str1)):
        up_left = 0
        for col in range(len(str2)):
            print(matrix_row)
            saved_current = matrix_row[col]

            if str1[row] == str2[col]:
                matrix_row[col] = 1 + up_left

                if matrix_row[col] > max_value:
                    max_value = matrix_row[col]
                    max_value_row = row

                else:
                    matrix_row[col] = 0

                up_left = saved_current

    start_index = max_value_row - max_value + 1
    return str1[start_index : max_value_row + 1]


# print(longest_common_substring("hello", "jello"))

l = ["A", "B"] + ["C"]

l.remove("A")


if type(l) == list:
    print('list')
