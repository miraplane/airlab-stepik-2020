N = int(input())

sensor = [[] for i in range(8)]
for n in range(N):
    l = list(map(int, input().strip().split()))
    for i in range(8):
        if l[i] > 50:
            sensor[i].append(0)
        else:
            sensor[i].append(1)

data = []
for i in range(8):
    start = sensor[i].index(1)
    end = len(sensor[i]) - list(reversed(sensor[i])).index(1)
    if (end - start) / 10 > len(data) / 10:
        data = sensor[i][start:end]

k = len(data) / 10
start = True
bin_str = ''
count = 0
for i in range(0, len(data)):
    if start:
        count = 0
        start = False
    count += 1
    
    if i != len(data) - 1 and data[i + 1] != data[i]:
        start = True
        bin_str += str(data[i]) * round(count / k)
    
    if i == len(data) - 1:
        bin_str += str(data[i]) * round(count / k)

start = bin_str.find('1') + 1
end = bin_str.rfind('1')
print(int(bin_str[start:end], 2))