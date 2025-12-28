# 一些内置函数
## defaultdict
```python
from collections import defaultdict
d1,d2=defaultdict(str),defaultdict(int)
d3,d4=defaultdict(list),defaultdict(set)
d2[1]+=1
#分别以空字符串，0，空列表，空集合为默认值
```
## lru_cache
```python
from functools import lru_cache
@lru_cache(maxsize=None)#表示缓存无限大
```
## deepcopy
浅拷贝，只复制对象本身，不复制对象内部的子对象，因此诸如二维数组之类的嵌套结构需要深拷贝
```python
import copy
l=[1,[2,3]]
l1=copy.deepcopy(l)
```
## operator
```python
import operator
op_dict={'+': operator.add,'-': operator.sub,'*': operator.mul,'/': operator.truediv,}
a=1
b=2
print(op_dict["+"](a,b))
print(op_dict["-"](op_dict["+"](a,b),b))
```
## 进制的转换
```python
num = 255
print(bin(num), oct(num), hex(num))
# 输出: 0b11111111 0o377 0xff
```
## 一次性读入
```python
# 导入sys模块，它提供了与Python解释器交互的功能
import sys
# 使用sys.stdin.read()一次性读取所有输入，直到遇到文件结束符（EOF）
# 这会把所有输入（包括换行符）作为一个大字符串返回
raw_input = sys.stdin.read()
# 打印原始输入，以便查看
print("原始输入内容：")
print(raw_input)
# 通常我们需要处理数据，比如按行分割成列表
# 使用splitlines()方法将字符串按行分割成列表，每行作为一个元素
lines = raw_input.splitlines()
# 打印分割后的行
print("分割后的行：")
for line in lines:
    print(line)
# 如果你想进一步处理每行的数据，比如每行有数字，可以转换
# 例如，假设每行是一个整数，可以这样转换：
# numbers = [int(line) for line in lines if line]  # 如果行不为空
```
## itertools
### permutations
```python
# 从n个元素中取出r个进行排列（考虑顺序）
items = ['A', 'B', 'C']
# 所有2个元素的排列
perms = itertools.permutations(items, 2)
print(list(perms))
# [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]
# 注意：AB和BA是不同的！
# 全排列（r不指定时默认为全部长度）
all_perms = itertools.permutations(items)
print(list(all_perms))  # 6种排列：ABC, ACB, BAC, BCA, CAB, CBA
```
### combinations
```python
# 从n个元素中取出r个进行组合（不考虑顺序）
items = ['A', 'B', 'C']
combs = itertools.combinations(items, 2)
print(list(combs))  # [('A', 'B'), ('A', 'C'), ('B', 'C')]
# 注意：只有3种！AB和BA被视为相同
# 应用：从5人中选3人组成委员会
people = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
teams = list(itertools.combinations(people, 3))
print(f"可以组成{len(teams)}个不同的3人委员会")
```
### combinations_with_replacement
```python
# 允许元素重复的组合
items = ['A', 'B']
combs = itertools.combinations_with_replacement(items, 2)
print(list(combs))  # [('A', 'A'), ('A', 'B'), ('B', 'B')]
# 注意：有('A', 'A')和('B', 'B')！
# 应用：从3种面值中取2枚硬币（可重复）
coins = [1, 5, 10]
combos = itertools.combinations_with_replacement(coins, 2)
for c in combos:
    print(f"{c} = {sum(c)}元")
```
## 日期与时间
```python
import calendar, datetime
print(calendar.isleap(2020))  # 输出: True
print(datetime.datetime(2023, 10, 5).weekday())  # 输出: 3 (星期四)
```
## count
序列.count(要查找的元素, 开始位置, 结束位置)
```python
# 示例1：统计数字出现次数
numbers = [1, 2, 3, 2, 4, 2, 5, 2]
count_2 = numbers.count(2)
print(f"数字2出现了 {count_2} 次")  # 输出：4
# 示例2：统计字符串出现次数
fruits = ["apple", "banana", "apple", "orange", "apple"]
count_apple = fruits.count("apple")
print(f"apple出现了 {count_apple} 次")  # 输出：3
# 示例3：统计布尔值出现次数
bool_list = [True, False, True, True, False]
count_true = bool_list.count(True)
print(f"True出现了 {count_true} 次")  # 输出：3
```
# 一些小的注意点
## sort
```python
l=[
{'name': 'Alice', 'score': 85, 'id': 3},
{'name': 'Bob', 'score': 92, 'id': 1},
{'name': 'Charlie', 'score': 85, 'id': 2},
{'name': 'Diana', 'score': 78, 'id': 4}
]

l.sort(key=lambda x:(-x[score],x[id]))
l1=sorted(l,key=lambda x:(-x[score],x[id]))
```
## 判断是不是数字,字母
```python
a=1,b="a"
if a.isdigit():#要求a纯数字
    print("YES")
if b.isalpha():#要求b纯字母
    print("YES")
```
## 大小写互换和转大写小写
```python
s="I like game."
result=s.swapcase()
result2=s.lower()
```
## rstrip,lstrip,strip
```python
a="   abc   "
b=a.rstrip();c=a.lstrip();d=a.strip()
#括号里也可以指定要删除什么字符
```
## replace
```python
s="abc"
s1=s.replace("a","b")
```
## find
```python
a="hello world hello"
a.find("hello"[, start[, end]])
#a为字符串，hello为子字符串，start，end可选。没找到返回-1，返回h的索引0
a.rfind("hello"[, start[, end]])
#从右边开始找，返回12
```
## 输出小数
```python
s=1/7
print("{:.2f}".format(s))
print(f"{s:.2f}")
```
## count
```python
s=" a a a "
print(s.count(" a "))
#输出2，因为第一个" a "数走后变成了"a a "
```
## 矩阵转置
```python
l=[[1,2,2],[1,3,3]]
l2=list(zip(*l))#此时l2里装的是元组
l3=[list(r) for r in zip(*l)]#此时l3里装的是列表
```
## enumerate
enumerate(iterable, start=0)
iterable：任何可迭代对象，比如列表、元组、字符串等。
start：索引的起始值，默认是0。
返回值：它返回一个枚举对象，每次迭代生成一个元组 (index, value)。
```python
a=["apple","banana","orange"]
b=list(enumerate(a,1))
#或者
for i,j in enumerate(a,1):
    print(i,j)
```
## 浮点数问题
int(a/b)向0取整，a//b向下取整，a//b中a,b有一个是浮点数，就会输出浮点数（但是数值还是整数），并且int会出现浮点数精度问题。另外，整数太大再进行乘除运算也可能会出现精度的问题。
## 时间复杂度问题
优先使用字典dict和集合set。
## 浮点数相等性的判断
math.isclose(a, b,  rel_tol=1e-09, abs_tol=0.0)
rel_tol相对容忍度
abs_tol绝对容忍度
要求abs(a-b)<=abs_tol或rel_tol*max(a,b)
# 并查集
## 并查集源码
```python
def init(n):
    parent=list(range(n))
    rank=[1]*n
    return parent,rank
def find(x):
    if parent[x]!=x:
        parent[x]=find(parent[x])
    return parent[x]
def union(x,y):
    root_x=find(x)
    root_y=find(y)
    if root_x==root_y:
        return False#指不需要合并
    if rank[root_x]<rank[root_y]:
        root_x,root_y=root_y,root_x
    parent[root_y]=root_x
    if rank[root_x]==rank[root_y]:
        rank[root_x]+=1
    return True#如果不需要返回这东西，就把前面的变成return，这里去掉
```
# greedy
## 区间问题
### 区间选点问题
按右端点排序，当左端点在右端点左边时加一个
### 最大不相交区间数目
按右端点排序，优先选择结束早的
### 区间覆盖问题
按左端点排序，每次选择能覆盖当前起点且终点最远的区域
### 区间分组问题
按左端点排序，然后用最小堆记录每一组的右端点
```python
intervals.sort(key=lambda x:x[0])
import heapq
min_heap=[]
for start,end in intervals:
    if min_heap and start >= min_heap[0]:
        heapq.heappop(min_heap)
    heapq.heappush(min_heap,end)
result=len(min_heap)
```
### 区间合并问题
按左端点排序，如果下一个区间的左端点在当前右端点右边，就再开一个区间
#### T29947校门外的树又来了
```python
l,m=map(int,input().split())
lst=[]
for i in range(m):
    a,b=map(int,input().split())
    lst.append([a,b])
lst.sort()
x=lst[0][0]
y=lst[0][1]
l1=[]
for i in lst:
    if i[0]<=y:
        y=max(y,i[1])
    else:
        l1.append([x,y])
        x=i[0]
        y=i[1]
l1.append([x,y])
print(l+1-sum(i[1]-i[0]+1 for i in l1))
```
# 二分查找
⼆分查找问题，需要注意 while 条件是 <，还是 <=。左指针赋值为 mid, mid+1, 还是 mid-1。 右指针赋值为
mid, mid+1, 还是 mid-1。
## biscet
### bisect介绍
```python
import bisect
l=[1,2,3,4,5,6,7,9,9]
a=bisect.bisect_left(l,7)
#bisect_left(l,num,le,ri)：在有序列表l中查找num的插入位置，假如num已经存在，返回第一个等于num的元素的位置，le，ri规定查找范围，默认le=0，ri=len(l)。
b=bisect.bisect_right(l,9)
#bisect_left(l,num,le,ri)：在有序列表l中查找num的插入位置，假如num已经存在，返回最后一个等于num的元素的位置。bisect.bisect与bisect.bisect_right一样。
bisect.insort_left(l,6)
bisect.insort_right(l,6)
#同上，先用bisect找出插入位置，再插入元素，保持列表有序。
```
### 求最长上升子序列
```python
import bisect
n = int(input())
*lis, = map(int, input().split())
dp = [1e9]*n
for i in lis:
    dp[bisect.bisect_left(dp, i)] = i
print(bisect.bisect_left(dp, 1e8))
```
# heap,queue,stack
## heap
```python
import heapq
heap=[1,3,2,4,7,3]
heapq.heapify(heap)
heapq.heappush(heap,1)
a=heapq.heappop(heap)
#最大堆用负数实现
#注意，堆不是排序，比如这里的原本的heap就满足堆的性质
```
### 用堆解决的问题
#### M18164剪绳子
```python
n=int(input())
import heapq as h
heap=list(map(int,input().split()))
h.heapify(heap)
s=0
while len(heap)>1:
    a=h.heappop(heap)+h.heappop(heap)
    h.heappush(heap,a)
    s+=a
print(s)
```
## 单调栈
### T26977接雨水
```python
def trap(height):
    """
    使用单调栈计算接雨水量
    :param height: 柱子高度数组
    :return: 能接的雨水量
    """
    if not height:
        return 0
    n = len(height)
    stack = []
    total_water = 0
    for i in range(n):
        current_height = height[i]
        while stack and current_height > height[stack[-1]]:
            bottom_idx = stack.pop()
            if not stack:
                break
            left_idx = stack[-1]
            left_height = height[left_idx]
            right_height = current_height
            h = min(left_height, right_height) - height[bottom_idx]
            w = i - left_idx - 1
            total_water += h * w
        stack.append(i)
    return total_water
```
# 筛法
## 埃氏筛
```python
def eratosthenes_sieve(n):
    """
    埃拉托斯特尼筛法 - 返回小于等于n的所有素数
    :param n: 上限
    :return: 素数列表
    """
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    primes = [i for i in range(2, n + 1) if is_prime[i]]
    return primes
```
## 欧拉筛
```python
def euler_sieve(n):
    """
    欧拉筛（线性筛） - 返回小于等于n的所有素数
    :param n: 上限
    :return: 素数列表
    """
    if n < 2:
        return []
    # 步骤1: 初始化
    is_prime = [True] * (n + 1)  # 标记数组
    primes = []  # 存储素数的列表
    is_prime[0] = is_prime[1] = False
    # 步骤2: 遍历2到n
    for i in range(2, n + 1):
        if is_prime[i]:  # 如果i是素数
            primes.append(i)  # 加入素数列表
        # 用当前已知的素数去标记i的倍数
        for p in primes:
            # 要标记的合数
            composite = i * p
            # 如果超过范围，停止
            if composite > n:
                break
            # 标记合数
            is_prime[composite] = False
            # 关键步骤：如果p能整除i，停止标记
            # 这是为了确保每个合数只被最小质因子标记一次
            if i % p == 0:
                break
    return primes
```
拓展：求最小质因子
```python
def sieve_min_prime_factors(n):
    """
    使用欧拉筛求每个数的最小质因子
    :param n: 上限
    :return: min_prime数组，min_prime[i]表示i的最小质因子
    """
    # 初始化
    min_prime = [0] * (n + 1)  # 0表示素数或未处理
    primes = []
    for i in range(2, n + 1):
        if min_prime[i] == 0:  # i是素数
            min_prime[i] = i  # 素数的最大质因子是自己
            primes.append(i)
        # 用已知素数标记合数
        for p in primes:
            if p > min_prime[i] or i * p > n:
                break
            min_prime[i * p] = p  # p是i*p的最小质因子
    return min_prime, primes
```
# dfs
## T01661帮助Jimmy
```python
for _ in range(int(input())):
    n,x0,y0,m=map(int,input().split())
    l=[]
    l.append([x0,x0,y0])
    l.append([-20000,20000,0])
    for i in range(n):
        l.append(list(map(int,input().split())))
    l.sort(key=lambda x:x[2])
    dp=[[float("inf"),float("inf")] for i in range(n+2)]
    dp[0]=[0,0]
    for i in range(1,n+2):
        y=l[i][2]
        for t in range(2):
            x=l[i][t]
            for j in range(i):
                if j!=0:
                    a,b,c=l[j][0],l[j][1],l[j][2]
                    if a<=x<=b and y-c<=m:
                        dp[i][t]=y-c+min(x-a+dp[j][0],b-x+dp[j][1])
                elif j==0:
                    c=l[j][2]
                    if y-c<=m:
                        dp[i][t]=y-c
    print(dp[-1][-1])
```
# bfs
写好visit即可
# Dijkstra
主要区别就是用heap代替bfs里的queue
# dp
## 01背包
```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity]
```
## 完全背包
```python
def knapsack_complete(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for i in range(len(weights)):
        for w in range(weights[i], capacity + 1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]
```
## 必须装满的完全背包
```python
def knapsack_complete_fill(weights, values, capacity):
    dp = [-float('inf')] * (capacity + 1)
    dp[0] = 0
    for i in range(len(weights)):
        for w in range(weights[i], capacity + 1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity] if dp[capacity] != -float('inf') else 0
```
## 状压dp
就是把状态用二进制表示
### T30201旅行售货商问题
```python
n=int(input())
d={}
for i in range(n):
    l=list(map(int,input().split()))
    d[i]=l
dp=[[float("inf")]*n for i in range(1<<n)]
dp[1][0]=0
for i in range(1,(1<<n)):
    for j in range(n):
        if dp[i][j]==float("inf"):
            continue
        for k in range(n):
            if ((i>>k) & 1)==0:
                newi=i|(1<<k)
                dp[newi][k]=min(dp[newi][k],dp[i][j]+d[j][k])
ans=float("inf")
for i in range(1,n):
    ans=min(ans,dp[-1][i]+d[i][0])
print(ans)
```
## 二重dp
用两个dp来记录
### T20744土豪购物
```python
l=list(map(int,input().split(",")))
n=len(l)
dp1=l[:]
dp2=l[:]
for i in range(1,n):
    dp1[i]=max(dp1[i],dp1[i]+dp1[i-1])
    dp2[i]=max(dp1[i-1],dp2[i-1]+dp2[i])
print(max(dp2))
```
# 双指针
## 快慢指针
### 判断是否存在环
```python
def is_happy(n):
    """
    判断一个数是否是快乐数
    使用快慢指针检测循环
    """
    def get_next(num):
        """计算下一个数（各位平方和）"""
        total = 0
        while num > 0:
            digit = num % 10  # 获取个位数
            total += digit * digit
            num //= 10  # 去掉个位
        return total
    # 快慢指针初始化
    slow = n
    fast = get_next(n)  # 快指针先走一步
    # 弗洛伊德判圈算法
    while fast != 1 and slow != fast:
        slow = get_next(slow)  # 慢指针走一步
        fast = get_next(get_next(fast))  # 快指针走两步
    # 如果fast最终变成1，就是快乐数
    return fast == 1
```
## 左右指针
寻找两数之和与要求一样
### 合并两个有序数组
```python
def merge_sorted_arrays(nums1, m, nums2, n):
    """
    将nums2合并到nums1中，nums1有足够空间
    nums1前m个元素有效，nums2有n个元素
    """
    # 从后往前合并
    i = m - 1  # nums1的最后一个有效元素
    j = n - 1  # nums2的最后一个元素
    k = m + n - 1  # 合并后的最后一个位置
    while i >= 0 and j >= 0:
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
    # 如果nums2还有剩余
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1
    return nums1
```
## 滑动窗口
一般是移动左右指针然后计数
### 颜色分类
```python
def sort_traffic_lights(lights):
    """
    原地整理红绿灯：0(红)在左，1(黄)在中，2(绿)在右
    """
    left = 0  # 红色灯的右边界
    current = 0  # 当前检查的灯
    right = len(lights) - 1  # 绿色灯的左边界
    while current <= right:
        if lights[current] == 0:  # 红灯故障
            # 交换到左边红色区域
            lights[left], lights[current] = lights[current], lights[left]
            left += 1
            current += 1
        elif lights[current] == 1:  # 黄灯正常
            # 保持在中间，直接跳过
            current += 1
        else:  # lights[current] == 2 绿灯正常
            # 交换到右边绿色区域
            lights[current], lights[right] = lights[right], lights[current]
            right -= 1
            # 注意：这里current不增加，因为交换过来的可能是0或1，需要再次检查
    return lights
```
# Manacher
```python
def manacher(s: str) -> str:
    """
    返回最长回文子串
    """
    if len(s) <= 1:
        return s
    # 1. 预处理字符串
    t = preprocess(s)
    n = len(t)
    # 2. 初始化P数组、C、R
    P = [0] * n  # P[i]存储以i为中心的回文半径
    C = 0  # 当前回文中心
    R = 0  # 当前回文右边界
    # 3. 遍历处理后的字符串
    for i in range(1, n - 1):  # 跳过开头的^和结尾的$
        # i_mirror是i关于C的对称点
        i_mirror = 2 * C - i  # 公式：C - (i - C)
        # 关键步骤1：利用对称性快速初始化P[i]
        if R > i:
            # i在R左边，可以利用对称性
            P[i] = min(R - i, P[i_mirror])
        else:
            # i在R右边（或等于），无法利用对称性
            P[i] = 0
        # 关键步骤2：中心扩展
        # 尝试扩展以i为中心的回文
        while (i + 1 + P[i] < n and  # 右边界不越界
               i - 1 - P[i] >= 0 and  # 左边界不越界
               t[i + 1 + P[i]] == t[i - 1 - P[i]]):  # 对称位置字符相等
            P[i] += 1
        # 关键步骤3：更新C和R
        if i + P[i] > R:
            C = i  # 更新中心
            R = i + P[i]  # 更新右边界
    # 4. 找到最长回文
    max_len = 0
    center_index = 0
    for i in range(1, n - 1):
        if P[i] > max_len:
            max_len = P[i]
            center_index = i
    # 5. 计算原字符串中的起始位置
    # 公式：(center_index - max_len) // 2
    start = (center_index - max_len) // 2
    return s[start:start + max_len]
```
# 前缀和
记录下前n个元素的sum方便后续计算
## T27141完美的爱
```python
from collections import defaultdict
def find_max_value(n, gifts):
    target_average = 520
    # 计算需要的偏移􁰁使得⽬标变为0
    gifts_offset = [x - target_average for x in gifts]
    prefix_sum = 0
    max_length = 0
    sum_indices = defaultdict(list)
    sum_indices[0].append(-1) # 初始化，表示从开始到-1的和为0
    for i, gift in enumerate(gifts_offset):
        prefix_sum += gift
        if prefix_sum in sum_indices:
            # 如果当前前缀和之前出现过，说明存在⼀个⼦数组其元素平均值为target_average
            length = i - sum_indices[prefix_sum][0] # 取最早的索引来获得最⻓的⼦数组
            max_length = max(max_length, length)
        sum_indices[prefix_sum].append(i)
    # 计算最⼤⼦数组的总和
    max_value = max_length * target_average if max_length > 0 else 0
    return max_value
# 读取输⼊
n = int(input())
gifts = list(map(int, input().split()))
# 计算结果
result = find_max_value(n, gifts)
print(result)
```
# sorting
## 1.冒泡排序
```python
def bubble_sort(s):
    n=len(s)
    f=True
    for i in range(n-1):
        f=False
        for j in range(n-i-1):
            if s[j]>s[j+1]:
                s[j],s[j+1]=s[j+1],s[j]
                f=True
        if f==False:
            break
    return s
```
## 2.归并排序
```python
def merge_sort(s):
    if len(s)<=1:
        return s
    mid=len(s)//2
    left=merge_sort(s[:mid])
    right=merge_sort(s[mid:])
    return merge(left,right)
def merge(l,r):
    ans=[]
    i=j=0
    while i<len(l) and j<len(r):
        if l[i]<r[j]:
            ans.append(l[i])
            i+=1
        else:
            ans.append(r[j])
            j+=1
    ans.extend(l[i:])
    ans.extend(r[j:])
    return ans
```
## 3.快速排序
```python
def quick_sort(s):
    if len(s)<=1:
        return s
    base=s[0]
    left=[x for x in s[1:] if x<base]
    right=[x for x in s[1:] if x>=base]
    return quick_sort(left)+[base]+quick_sort(right)
```