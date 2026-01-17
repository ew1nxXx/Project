import tkinter as tk
import random
from tkinter import HORIZONTAL

# Dimensions for the canvas area
WIDTH = 900
HEIGHT = 600

# Color palette for bar states
BAR_COLOR = "#00BFFF"
BAR_ACTIVE = "#FF4500"
BAR_DONE = "#32CD32"

bars = []
bar_values = []
sort_process = None  # This will be a generator when sorting

ALGORITHMS = ["Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort"]

def draw_bar(index, value, color):
    x_start = index * bar_width
    x_end = x_start + bar_width
    y_end = HEIGHT
    y_start = HEIGHT - value
    canvas.coords(bars[index], x_start, y_start, x_end, y_end)
    canvas.itemconfig(bars[index], fill=color)

def color_all_bars(color):
    for idx in range(len(bar_values)):
        draw_bar(idx, bar_values[idx], color)

# A very classic insertion sort implementation
def insertion_sort():
    for i in range(1, len(bar_values)):
        current = bar_values[i]
        j = i - 1
        while j >= 0 and bar_values[j] > current:
            bar_values[j + 1] = bar_values[j]
            draw_bar(j + 1, bar_values[j + 1], BAR_ACTIVE)
            yield
            draw_bar(j + 1, bar_values[j + 1], BAR_COLOR)
            j -= 1
        bar_values[j + 1] = current
        draw_bar(j + 1, current, BAR_ACTIVE)
        yield
        draw_bar(j + 1, current, BAR_COLOR)
    color_all_bars(BAR_DONE)

# Merge sort uses a recursive breakdown
def merge_sort():
    yield from merge_sort_helper(0, len(bar_values) - 1)
    color_all_bars(BAR_DONE)

def merge_sort_helper(left, right):
    if left < right:
        middle = (left + right) // 2
        yield from merge_sort_helper(left, middle)
        yield from merge_sort_helper(middle + 1, right)
        yield from merge_subarrays(left, middle, right)

def merge_subarrays(left, mid, right):
    left_part = bar_values[left:mid+1]
    right_part = bar_values[mid+1:right+1]

    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            bar_values[k] = left_part[i]
            i += 1
        else:
            bar_values[k] = right_part[j]
            j += 1
        draw_bar(k, bar_values[k], BAR_ACTIVE)
        yield
        draw_bar(k, bar_values[k], BAR_COLOR)
        k += 1

    while i < len(left_part):
        bar_values[k] = left_part[i]
        draw_bar(k, bar_values[k], BAR_ACTIVE)
        yield
        draw_bar(k, bar_values[k], BAR_COLOR)
        i += 1
        k += 1

    while j < len(right_part):
        bar_values[k] = right_part[j]
        draw_bar(k, bar_values[k], BAR_ACTIVE)
        yield
        draw_bar(k, bar_values[k], BAR_COLOR)
        j += 1
        k += 1

def quick_sort():
    yield from quick_sort_helper(0, len(bar_values) - 1)
    color_all_bars(BAR_DONE)

def quick_sort_helper(low, high):
    if low < high:
        pivot_index = yield from partition(low, high)
        yield from quick_sort_helper(low, pivot_index - 1)
        yield from quick_sort_helper(pivot_index + 1, high)

def partition(low, high):
    pivot_val = bar_values[high]
    i = low
    for j in range(low, high):
        if bar_values[j] <= pivot_val:
            bar_values[i], bar_values[j] = bar_values[j], bar_values[i]
            draw_bar(i, bar_values[i], BAR_ACTIVE)
            draw_bar(j, bar_values[j], BAR_ACTIVE)
            yield
            draw_bar(i, bar_values[i], BAR_COLOR)
            draw_bar(j, bar_values[j], BAR_COLOR)
            i += 1

    bar_values[i], bar_values[high] = bar_values[high], bar_values[i]
    draw_bar(i, bar_values[i], BAR_ACTIVE)
    draw_bar(high, bar_values[high], BAR_ACTIVE)
    yield
    draw_bar(i, bar_values[i], BAR_COLOR)
    draw_bar(high, bar_values[high], BAR_COLOR)
    return i

def heap_sort():
    n = len(bar_values)

    # Build the heap (in-place, yay)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)

    # Extract elements one by one
    for end in range(n - 1, 0, -1):
        bar_values[0], bar_values[end] = bar_values[end], bar_values[0]
        draw_bar(0, bar_values[0], BAR_ACTIVE)
        draw_bar(end, bar_values[end], BAR_ACTIVE)
        yield
        draw_bar(0, bar_values[0], BAR_COLOR)
        draw_bar(end, bar_values[end], BAR_COLOR)
        yield from heapify(end, 0)

    color_all_bars(BAR_DONE)

def heapify(size, root):
    largest = root
    left = 2 * root + 1
    right = 2 * root + 2

    if left < size and bar_values[left] > bar_values[largest]:
        largest = left
    if right < size and bar_values[right] > bar_values[largest]:
        largest = right

    if largest != root:
        bar_values[root], bar_values[largest] = bar_values[largest], bar_values[root]
        draw_bar(root, bar_values[root], BAR_ACTIVE)
        draw_bar(largest, bar_values[largest], BAR_ACTIVE)
        yield
        draw_bar(root, bar_values[root], BAR_COLOR)
        draw_bar(largest, bar_values[largest], BAR_COLOR)
        yield from heapify(size, largest)

# Starts sorting animation
def begin_sort():
    global sort_process
    color_all_bars(BAR_COLOR)
    selected = algorithm_choice.get()

    if selected == "Insertion Sort":
        sort_process = insertion_sort()
    elif selected == "Merge Sort":
        sort_process = merge_sort()
    elif selected == "Quick Sort":
        sort_process = quick_sort()
    else:
        sort_process = heap_sort()
    animate_step()

def animate_step():
    global sort_process
    if sort_process:
        try:
            next(sort_process)
            root.after(speed_slider.get(), animate_step)
        except StopIteration:
            sort_process = None

# Generates the bars with randomized values
def reset_bars():
    global bars, bar_values, bar_width, sort_process
    sort_process = None
    canvas.delete("all")
    bars = []
    bar_values = []

    num_bars = size_slider.get()
    bar_width = WIDTH // num_bars
    data = list(range(1, num_bars + 1))
    random.shuffle(data)

    for i, val in enumerate(data):
        height = val * (HEIGHT // num_bars)  # Just a scaling factor
        bar_values.append(height)
        bars.append(canvas.create_rectangle(0, 0, 0, 0, fill=BAR_COLOR))
        draw_bar(i, height, BAR_COLOR)

# GUI setup
root = tk.Tk()
root.title("Sorting Visualizer")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

controls = tk.Frame(root)
controls.pack()

# Generate new dataset
tk.Button(controls, text="Generate", width=12, command=reset_bars).grid(row=0, column=0)

algorithm_choice = tk.StringVar()
algorithm_choice.set(ALGORITHMS[0])
tk.OptionMenu(controls, algorithm_choice, *ALGORITHMS).grid(row=0, column=1)

# Start sorting
tk.Button(controls, text="Sort", width=12, command=begin_sort).grid(row=0, column=2)

# Size and speed sliders
size_slider = tk.Scale(controls, from_=10, to=80, orient=HORIZONTAL, label="Size")
size_slider.set(30)
size_slider.grid(row=1, column=0, columnspan=2)

speed_slider = tk.Scale(controls, from_=5, to=200, orient=HORIZONTAL, label="Speed")
speed_slider.set(30)
speed_slider.grid(row=1, column=2)

reset_bars()
root.mainloop()
