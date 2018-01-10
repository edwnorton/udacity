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
任务2: 哪个电话号码的通话总时间最长? 不要忘记，用于接听电话的时间也是通话时间的一部分。
输出信息:
"<telephone number> spent the longest time, <total time> seconds, on the phone during
September 2016.".

提示: 建立一个字典，并以电话号码为键，通话总时长为值。
这有利于你编写一个以键值对为输入，并修改字典的函数。
如果键已经存在于字典内，为键所对应的值加上对应数值；
如果键不存在于字典内，将此键加入字典，并将它的值设为给定值。
"""


def num_time_count(calllist):
    call_time = {}
    """
    建立一个字典，以电话号码为键，通话时长为值
    """
    for num in calllist:
        if num[0] not in call_time:#如果号码不在字典中，加入该号码到字典中
            call_time[num[0]] = num[3]
        else:#如果号码在字典中，加入该号码的通话时长
            call_time[num[0]] = int(call_time[num[0]]) + int(num[3])
    for num in calllist:
        if num[1] not in call_time:
            call_time[num[1]] = num[3]
        else:
            call_time[num[1]] = int(call_time[num[1]]) + int(num[3])
    return call_time
#print (num_time_count(calls))
Sort_calltime = sorted(num_time_count(calls).items(), key=lambda item:int(item[1]), reverse=True)
#print(Sort_calltime)
print ("{} spent the longest time, {} seconds, on the phone during September 2016.".format(Sort_calltime[0][0], Sort_calltime[0][1]))

