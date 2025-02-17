#Ex7_1.py
import turtle as t

t.title('自动轨迹绘制')
t.setup(800, 600, 0, 0)
t.pencolor("red")
t.pensize(5)
#数据读取
datals = []
f = open("data.txt") #打开文件data
for line in f:
    line = line.replace("\n","")
    datals.append(list(map(eval, line.split(",")))) #逐行添加文本中的数据，通过“，”将字符串分割成数组
f.close()
#自动绘制
for i in range(len(datals)):
    t.pencolor(datals[i][3],datals[i][4],datals[i][5])
    t.fd(datals[i][0])
    if datals[i][1]:
        t.rt(datals[i][2])
    else:
        t.lt(datals[i][2])
        
t.done()
