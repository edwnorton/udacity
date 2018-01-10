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
任务4:
电话公司希望辨认出可能正在用于进行电话推销的电话号码。
找出所有可能的电话推销员:
这样的电话总是向其他人拨出电话，
但从来不发短信、接收短信或是收到来电


请输出如下内容
"These numbers could be telemarketers: "
<list of numbers>
电话号码不能重复，每行打印一条，按字典顺序排序后输出。
"""
def Call_list(column, csv):
    """
    :param column: csv中列数据
    :param csv: 给定的整个数据
    :return: 返回一个list
    """
    num_list = []
    for num in csv:
        num_list.append(num[column])
    return num_list
def extract_num():
    Caller = []
    num_list = []
    """
    去除Caller中重复数据
    """
    for num in calls:
        if num[0] not in Caller:
            Caller.append(num[0])
        else:
            pass
    Called = Call_list(1, calls)
    tcaller = Call_list(0, texts)
    tcalled = Call_list(1, texts)
    num_list = Called + tcalled + tcaller
    #print(len(Caller))
    """
    排除非营销号码
    """
    for num in num_list:
        if num in Caller:
            Caller.remove(num)
        else:
            pass
    #print(len(Caller))
    #print(len(num_list))
    return Caller
print("These numbers could be telemarketers: ")
for i in extract_num():
    print(i)


