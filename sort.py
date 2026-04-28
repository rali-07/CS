import tkinter as tk
import random
import re
import time
from tkinter import scrolledtext
from tkinter import ttk


# ---------- 主窗口 ----------
root = tk.Tk()
root.title("排序可视化")
root.geometry("1200x700")
root.configure(bg="black")

# ---------- 全局数据 ----------
data = []                   # 当前数据列表
sorting = False             # 是否正在排序中
sort_generator = None       # 当前排序算法的生成器
delay = 50                  # 排序每步延迟（毫秒）
last_random_n = 20          # 上次成功生成随机数据的数量（用于输入框回退）

# 绘图缓存
_rect_ids = []              # 存储每个柱子的矩形ID
_line_id = None             # 底部参考线ID
_text_max_id = None         # 最大值文字ID
_text_n_id = None           # 数据量文字ID
_last_n = 0                 # 上一次数据量（用于检测是否重建图形）


# ---------- 日志函数 ----------
def log_message(msg, color='#aaa'):
    """向日志框追加一条消息，并自动滚动到底部"""
    log_text.config(state='normal')
    timestamp = time.strftime("%H:%M:%S")
    log_text.insert(tk.END, f"[{timestamp}] {msg}\n")
    log_text.tag_config(color, foreground=color)
    start = log_text.index("end-2l linestart")
    end = log_text.index("end-1c")
    log_text.tag_add(color, start, end)
    log_text.see(tk.END)
    log_text.config(state='disabled')


# ---------- 重置排序状态 ----------
def reset_sort_state():
    """清空生成器并停止排序，用于数据/算法变更时"""
    global sort_generator, sorting
    if sorting:
        sorting = False
    sort_generator = None
    btn_start_sort.config(state='normal')
    btn_stop_sort.config(state='disabled')
    draw_bars()                     # 清除高亮，但保留数据


# ---------- 无闪烁绘图函数 ----------
def draw_bars(highlight=None):
    """
    根据全局 data 绘制柱形图，支持高亮索引列表。
    采用缓存机制，只在数据量改变时重建图形，平时仅更新坐标和颜色，避免闪烁。
    """
    global canvas, data, _rect_ids, _line_id, _text_max_id, _text_n_id, _last_n

    # 无数据时显示提示并清空缓存
    if not data:
        canvas.delete("all")
        _rect_ids.clear()
        _line_id = None
        _text_max_id = None
        _text_n_id = None
        canvas.create_text(
            canvas.winfo_width() // 2,
            canvas.winfo_height() // 2,
            text="暂无数据，请生成或导入数据",
            fill="gray",
            font=("Arial", 14)
        )
        return

    # 获取画布最新尺寸
    canvas.update_idletasks()
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    n = len(data)
    max_val = max(data)
    bottom_margin = 20
    draw_height = h - bottom_margin
    bar_width = w / n

    highlight_set = set(highlight) if highlight else set()

    # 数据量改变 → 重建所有图形
    if n != _last_n or len(_rect_ids) != n:
        canvas.delete("all")
        _rect_ids.clear()
        for i, value in enumerate(data):
            x0 = i * bar_width
            x1 = x0 + bar_width
            bar_height = (value / max_val) * draw_height
            y0 = h - bottom_margin - bar_height
            y1 = h - bottom_margin
            rid = canvas.create_rectangle(
                x0, y0, x1, y1,
                fill='white', outline='white', width=1
            )
            _rect_ids.append(rid)
        _line_id = canvas.create_line(
            0, h - bottom_margin, w, h - bottom_margin,
            fill='gray', width=1, dash=(4, 2)
        )
        _text_max_id = canvas.create_text(
            5, 15, anchor='nw', text=f"最大值: {max_val}",
            fill='#ff00ff', font=('Arial', 10, 'bold')
        )
        _text_n_id = canvas.create_text(
            5, 30, anchor='nw', text=f"数据量: {n}",
            fill='#ff00ff', font=('Arial', 10, 'bold')
        )
    else:
        # 数据量未变：只更新现有矩形的坐标、颜色以及参考线和文字
        for i, (value, rid) in enumerate(zip(data, _rect_ids)):
            x0 = i * bar_width
            x1 = x0 + bar_width
            bar_height = (value / max_val) * draw_height
            y0 = h - bottom_margin - bar_height
            y1 = h - bottom_margin
            canvas.coords(rid, x0, y0, x1, y1)
            fill_color = 'red' if i in highlight_set else 'white'
            outline_color = 'red' if i in highlight_set else 'white'
            canvas.itemconfig(rid, fill=fill_color, outline=outline_color)
        canvas.coords(_line_id, 0, h - bottom_margin, w, h - bottom_margin)
        canvas.itemconfig(_text_max_id, text=f"最大值: {max_val}")
        canvas.itemconfig(_text_n_id, text=f"数据量: {n}")

    _last_n = n


# ---------- 数据生成与导入 ----------
def generate_random_data():
    """从输入框读取数量，生成随机顺序的 1..n 数据"""
    global data, last_random_n
    reset_sort_state()          # 新数据 → 丢弃旧排序进度
    try:
        raw = size_entry.get().strip()
        if not raw:
            size_entry.delete(0, tk.END)
            size_entry.insert(0, str(last_random_n))
            log_message("请输入有效数据！", 'red')
            return

        n = int(raw)
        if n <= 0:
            size_entry.delete(0, tk.END)
            size_entry.insert(0, str(last_random_n))
            log_message("数量必须为正整数，已恢复上次有效值", 'red')
            return

        if n > 2000:
            log_message(f"输入数量 {n} 超过上限2000，已自动调整为2000", 'orange')
            n = 2000
            size_entry.delete(0, tk.END)
            size_entry.insert(0, str(n))

        data = [i for i in range(1, n + 1)]
        random.shuffle(data)
        log_message(f"已生成大小为 {n} 的随机数据", 'lightgreen')
        draw_bars()
        last_random_n = n

    except ValueError:
        size_entry.delete(0, tk.END)
        size_entry.insert(0, str(last_random_n))
        log_message("请输入有效的整数！", 'red')
        return


def import_data():
    """从输入框读取数字（支持逗号、空格混合分隔），转换为整数列表"""
    global data
    reset_sort_state()
    s = import_entry.get().strip()
    if not s:
        log_message("请输入有效数据！", 'red')
        return

    parts = re.findall(r"\d+", s)          # 提取所有连续数字
    if not parts:
        log_message("未找到任何数字！", 'red')
        return

    nums = []
    for part in parts:
        num = int(part)
        if num <= 0:
            log_message(f"数字{num}过小，已自动调整为1", 'orange')
            num = 1
        if num > 2000:
            log_message(f"数字{num}过大，已自动调整为2000", 'orange')
            num = 2000
        nums.append(num)

    if len(nums) > 2000:
        log_message("数据量过大，已自动调整为2000", 'orange')
        nums = nums[:2000]

    data = nums
    preview = ', '.join(str(x) for x in data[:6])
    if len(data) > 6:
        preview += '...'
    log_message(f"已导入 {len(data)} 个数据：{preview}", 'lightgreen')
    draw_bars()


# ---------- 速度控制 ----------
def update_delay_from_scale(val):
    """滑动条拖动时的回调"""
    global delay
    delay = int(float(val))
    speed_entry.delete(0, tk.END)
    speed_entry.insert(0, str(delay))
    log_message(f"排序延迟设为 {delay} 毫秒", '#aaa')


def update_delay_from_entry(event=None):
    """输入框手动输入后的回调（回车或失去焦点）"""
    global delay
    try:
        new_delay = int(speed_entry.get())
        if new_delay < 1:
            new_delay = 1
            log_message("速度不能小于1毫秒，已自动设为1", 'orange')
        elif new_delay > 1000:
            new_delay = 1000
            log_message("速度不能大于1000毫秒，已自动设为1000", 'orange')
        else:
            log_message(f"排序延迟设为 {new_delay} 毫秒", '#aaa')
        delay = new_delay
        speed_scale.set(delay)
        speed_entry.delete(0, tk.END)
        speed_entry.insert(0, str(delay))
    except ValueError:
        speed_entry.delete(0, tk.END)
        speed_entry.insert(0, str(delay))
        log_message(f"请输入1~1000之间的整数 (当前为 {delay})", 'red')


# ---------- 排序算法生成器 ----------
def bubble_sort_generator(arr):
    """冒泡排序，每次交换时 yield 两个索引"""
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                yield (j, j + 1)
        if not swapped:
            log_message(f"第 {i+1} 轮未发生交换，提前结束", '#aaa')
            break
    yield None


def merge_sort_generator(arr):
    """归并排序（自底向上），每次合并后 yield 整个合并区间的索引列表"""
    n = len(arr)
    width = 1
    temp = [0] * n

    while width < n:
        left = 0
        while left < n:
            mid = min(left + width - 1, n - 1)
            right = min(left + 2 * width - 1, n - 1)
            i, j, k = left, mid + 1, left
            while i <= mid and j <= right:
                if arr[i] <= arr[j]:
                    temp[k] = arr[i]
                    i += 1
                else:
                    temp[k] = arr[j]
                    j += 1
                k += 1
            while i <= mid:
                temp[k] = arr[i]
                i += 1
                k += 1
            while j <= right:
                temp[k] = arr[j]
                j += 1
                k += 1
            for idx in range(left, right + 1):
                arr[idx] = temp[idx]
            yield list(range(left, right + 1))
            left += 2 * width
        width *= 2
    yield None


def selection_sort_generator(arr):
    """选择排序，每次交换时 yield 两个索引"""
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield (i, min_idx)
    yield None


def insertion_sort_generator(arr):
    """插入排序，每次移动元素时 yield 两个索引"""
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            yield (j, j + 1)
            j -= 1
        arr[j + 1] = key
    yield None


def quick_sort_generator(arr):
    """快速排序（迭代栈版本），每次交换或 pivot 归位时 yield 两个索引"""
    n = len(arr)
    stack = [(0, n - 1)]
    while stack:
        left, right = stack.pop()
        if left >= right:
            continue
        pivot = arr[left]
        i, j = left, right
        while i < j:
            while i < j and arr[j] >= pivot:
                j -= 1
            if i < j:
                arr[i] = arr[j]
                yield (i, j)
            while i < j and arr[i] <= pivot:
                i += 1
            if i < j:
                arr[j] = arr[i]
                yield (i, j)
        arr[i] = pivot
        yield (i, left)
        stack.append((left, i - 1))
        stack.append((i + 1, right))
    yield None


def heap_sort_generator(arr):
    """堆排序（合并版），每次堆化只高亮最终交换的起始和结束位置"""
    n = len(arr)

    def heapify(n, i):
        """对以 i 为根的子树进行堆化，如果有交换则返回 (start_i, final_i)，否则 None"""
        start_i = i
        while True:
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n and arr[left] > arr[largest]:
                largest = left
            if right < n and arr[right] > arr[largest]:
                largest = right
            if largest == i:
                break
            arr[i], arr[largest] = arr[largest], arr[i]
            i = largest
        if i != start_i:
            return (start_i, i)
        return None

    # 建堆
    for i in range(n // 2 - 1, -1, -1):
        res = heapify(n, i)
        if res:
            yield res

    # 排序
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        yield (0, i)
        res = heapify(i, 0)
        if res:
            yield res
    yield None


def shell_sort_generator(arr):
    """希尔排序，每次移动元素时 yield 两个索引"""
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                yield (j, j - gap)
                j -= gap
            arr[j] = temp
        gap //= 2
    yield None


def monkey_sort_generator(arr):
    """猴子排序（Bogo Sort）——仅供娱乐，效率极低"""
    import random
    n = len(arr)
    if n <= 1:
        yield None
        return

    max_attempts = 10000 * n       # 最大尝试次数，防止卡死
    attempt = 0

    def is_sorted():
        for i in range(n - 1):
            if arr[i] > arr[i + 1]:
                return False
        return True

    if is_sorted():
        yield None
        return

    while attempt < max_attempts:
        random.shuffle(arr)
        yield list(range(n))          # 高亮所有柱子（表示一次随机洗牌）
        if is_sorted():
            log_message(f"猴王在 {attempt+1} 次尝试后成功！", 'lightgreen')
            break
        attempt += 1
        if attempt % 100 == 0:
            log_message(f"猴王已尝试 {attempt} 次...", '#aaa')
    else:
        log_message(f"猴王尝试超过 {max_attempts} 次，已放弃", 'red')
    yield None


# ---------- 排序执行流程 ----------
def start_sort():
    """开始排序：若有未完成的生成器则继续，否则根据当前算法创建新生成器"""
    global sorting, sort_generator
    if sorting:
        log_message("排序进行中，请勿重复点击", 'orange')
        return
    if not data:
        log_message("没有数据，请先生成或导入数据", 'red')
        return

    # 继续上一次暂停的排序
    if sort_generator is not None:
        log_message("继续之前的排序...", 'lightblue')
        sorting = True
        btn_start_sort.config(state='disabled')
        btn_stop_sort.config(state='normal')
        step_sort()
        return

    # 根据选择的算法创建新生成器
    selected_algo = algo_combo.get()
    log_message(f"开始执行 {selected_algo}...", 'lightblue')

    if selected_algo == "冒泡排序":
        sort_generator = bubble_sort_generator(data)
    elif selected_algo == "归并排序":
        sort_generator = merge_sort_generator(data)
    elif selected_algo == "选择排序":
        sort_generator = selection_sort_generator(data)
    elif selected_algo == "插入排序":
        sort_generator = insertion_sort_generator(data)
    elif selected_algo == "快速排序":
        sort_generator = quick_sort_generator(data)
    elif selected_algo == "堆排序":
        sort_generator = heap_sort_generator(data)
    elif selected_algo == "希尔排序":
        sort_generator = shell_sort_generator(data)
    elif selected_algo == "猴子排序":
        sort_generator = monkey_sort_generator(data)
        if len(data) > 8:
            log_message("猴王挠了挠头，祝你好运", 'orange')
    else:
        log_message(f"未知算法: {selected_algo}", 'red')
        return

    sorting = True
    btn_start_sort.config(state='disabled')
    btn_stop_sort.config(state='normal')
    step_sort()


def step_sort():
    """排序的每一步：调用生成器，重绘高亮，然后通过 after 安排下一步"""
    global sorting, sort_generator, delay
    if not sorting or sort_generator is None:
        return
    try:
        result = next(sort_generator)
    except StopIteration:
        finish_sort()
        return

    if result is None:
        finish_sort()
        return

    draw_bars(highlight=list(result))
    root.after(delay, step_sort)


def finish_sort():
    """排序正常结束，恢复界面状态"""
    global sorting, sort_generator
    sorting = False
    sort_generator = None
    log_message("排序完成！", 'lightgreen')
    draw_bars()
    btn_start_sort.config(state='normal')
    btn_stop_sort.config(state='disabled')


def stop_sort():
    """暂停排序（保留生成器，可继续）"""
    global sorting
    if not sorting:
        log_message("当前没有正在进行的排序", 'orange')
        return
    sorting = False
    log_message("排序已暂停，点击「开始排序」继续", 'orange')
    draw_bars()                     # 清除高亮
    btn_start_sort.config(state='normal')
    btn_stop_sort.config(state='disabled')


def on_algo_changed(event=None):
    """切换算法时重置排序状态，并输出趣味提示"""
    reset_sort_state()
    t = algo_combo.get()
    log_message(f"切换到算法：{t}", '#aaa')
    if t == "猴子排序":
        log_message("🐒 呜呼～ 猴王登场！", 'orange')


# ---------- 界面布局 ----------
main_container = tk.Frame(root, bg="black")
main_container.pack(fill='both', expand=True)

left_frame = tk.Frame(main_container, bg="black")
left_frame.pack(side='left', fill='both', expand=True)

right_frame = tk.Frame(main_container, width=180, bg='#2b2b2b')
right_frame.pack(side='right', fill='y')
right_frame.pack_propagate(False)          # 固定宽度

canvas = tk.Canvas(left_frame, bg='#1e1e1e', highlightthickness=0)
canvas.pack(pady=10, padx=10, fill='both', expand=True)

# ----- 数据数量 -----
tk.Label(right_frame, text="数据数量", fg='white', bg='#2b2b2b',
         font=('Arial', 10)).pack(pady=(10, 0), fill='x')
size_entry = tk.Entry(right_frame, bg='#3c3f41', fg='white', insertbackground='white')
size_entry.pack(pady=5, fill='x')
size_entry.insert(0, "20")

btn_random = tk.Button(right_frame, text="生成随机数据",
                       command=generate_random_data,
                       bg='#3c3f41', fg='white', activebackground='#555')
btn_random.pack(pady=5, fill='x')

# ----- 导入数据 -----
tk.Label(right_frame, text="导入数据 (逗号/空格分隔)", fg='white', bg='#2b2b2b',
         font=('Arial', 10)).pack(pady=(10, 0), fill='x')
import_entry = tk.Entry(right_frame, bg='#3c3f41', fg='white', insertbackground='white')
import_entry.pack(pady=5, fill='x')
import_entry.insert(0, "5,12,8,20,15")
btn_import = tk.Button(right_frame, text="导入数据",
                       command=import_data,
                       bg='#3c3f41', fg='white', activebackground='#555')
btn_import.pack(pady=5, fill='x')

# ----- 速度控制 -----
speed_frame = tk.Frame(right_frame, bg='#2b2b2b')
speed_frame.pack(pady=(10, 0), fill='x')
tk.Label(speed_frame, text="排序速度 (毫秒/步)", fg='white', bg='#2b2b2b',
         font=('Arial', 9)).pack(anchor='w')
speed_control_frame = tk.Frame(right_frame, bg='#2b2b2b')
speed_control_frame.pack(pady=5, fill='x')
speed_scale = tk.Scale(speed_control_frame, from_=1, to=1000, orient='horizontal',
                       bg='#2b2b2b', fg='white', highlightthickness=0,
                       command=update_delay_from_scale)
speed_scale.pack(side='left', fill='x', expand=True)
speed_scale.set(50)
speed_entry = tk.Entry(speed_control_frame, width=6, bg='#3c3f41', fg='white',
                       insertbackground='white', justify='center')
speed_entry.pack(side='right', padx=(5, 0))
speed_entry.insert(0, "50")
speed_entry.bind('<Return>', update_delay_from_entry)
speed_entry.bind('<FocusOut>', update_delay_from_entry)

# ----- 排序算法选择 -----
tk.Label(right_frame, text="排序算法", fg='white', bg='#2b2b2b',
         font=('Arial', 9)).pack(pady=(10, 0), fill='x')
algo_var = tk.StringVar()
algo_combo = ttk.Combobox(right_frame, textvariable=algo_var,
                          values=["冒泡排序", "归并排序", "选择排序",
                                  "插入排序", "快速排序", "堆排序",
                                  "希尔排序", "猴子排序"],
                          state="readonly", font=('Arial', 9))
algo_combo.pack(pady=5, fill='x')
algo_combo.current(0)
algo_combo.bind('<<ComboboxSelected>>', on_algo_changed)

# ----- 开始/停止按钮 -----
btn_start_sort = tk.Button(right_frame, text="开始排序",
                           command=start_sort,
                           bg='#3c3f41', fg='white', activebackground='#555')
btn_start_sort.pack(pady=5, fill='x')
btn_stop_sort = tk.Button(right_frame, text="停止排序",
                          command=stop_sort,
                          bg='#3c3f41', fg='white', activebackground='#555')
btn_stop_sort.pack(pady=5, fill='x')
btn_stop_sort.config(state='disabled')

# ----- 日志框 -----
log_frame = tk.Frame(right_frame, bg='#2b2b2b')
log_frame.pack(pady=(10, 0), fill='both', expand=True)
tk.Label(log_frame, text="日志信息", fg='white', bg='#2b2b2b',
         font=('Arial', 9, 'bold')).pack(anchor='w')
log_text = scrolledtext.ScrolledText(log_frame, height=8, bg='#1e1e1e', fg='white',
                                     insertbackground='white', font=('Consolas', 8),
                                     wrap=tk.WORD, relief='flat')
log_text.pack(fill='both', expand=True, pady=(2, 0))
log_text.config(state='disabled')

# ---------- 启动主循环 ----------
root.mainloop()