"""
下面的文件将会从csv文件中读取读取短信与电话记录，
你将在以后的课程中了解更多有关读取文件的知识。
"""
import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)


"""
任务1：
短信和通话记录中一共有多少电话号码？每个号码只统计一次。
输出信息：
"There are <count> different telephone numbers in the records."
"""

"""
1.extract all data,and put the data in num_list
"""
num_list = []
for text_num in texts:
    num_list.append(text_num[0])
    num_list.append(text_num[1])
for calls_num in calls:
    num_list.append(calls_num[0])
    num_list.append(calls_num[1])
"""
2.count the different numbers
"""
def count_num(list):
    diff_num_count = []
    for num in list:
        if num not in diff_num_count:
            diff_num_count.append(num)
        else:
            pass
    return len(diff_num_count)
print ("There are {} different telephone numbers in the records.".format(count_num(num_list)))
