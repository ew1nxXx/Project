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

ALGORITHMS = ["Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort"]

class SortingVisualizer:
    """
    SortingVisualizer is the main class that manages the GUI,
    program state, and sorting animations.

    It creates the tkinter window, draws the bars, and runs
    different sorting algorithms step by step using generators.
    """
    def __init__(self):
        self.bars = []
        self.bar_values = []
        self.sort_process = None
        self.bar_width = 1

        self.root = tk.Tk()
        self.root.title("Sorting Visualizer")

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.controls = tk.Frame(self.root)
        self.controls.pack()

        tk.Button(self.controls, text="Generate", width=12, command=self.reset_bars).grid(row=0, column=0)

        self.algorithm_choice = tk.StringVar()
        self.algorithm_choice.set(ALGORITHMS[0])
        tk.OptionMenu(self.controls, self.algorithm_choice, *ALGORITHMS).grid(row=0, column=1)

        tk.Button(self.controls, text="Sort", width=12, command=self.begin_sort).grid(row=0, column=2)

        self.size_slider = tk.Scale(self.controls, from_=10, to=80, orient=HORIZONTAL, label="Size")
        self.size_slider.set(30)
        self.size_slider.grid(row=1, column=0, columnspan=2)

        self.speed_slider = tk.Scale(self.controls, from_=5, to=200, orient=HORIZONTAL, label="Speed")
        self.speed_slider.set(30)
        self.speed_slider.grid(row=1, column=2)

        self.reset_bars()
        self.root.mainloop()

    def draw_bar(self,index, value, color):
        """
    Draws or updates a single bar on the canvas.

    index: position of the bar
    value: height of the bar
    color: fill color of the bar
    """
        x_start = index * self.bar_width
        x_end = x_start + self.bar_width
        y_end = HEIGHT
        y_start = HEIGHT - value
        self.canvas.coords(self.bars[index], x_start, y_start, x_end, y_end)
        self.canvas.itemconfig(self.bars[index], fill=color)

    def color_all_bars(self,color):
        for idx in range(len(self.bar_values)):
            self.draw_bar(idx, self.bar_values[idx], color)

#insertion sort implementation
    def insertion_sort(self):
        """
    Generator implementation of insertion sort.
    Yields after each movement to allow animation.
    """
        for i in range(1, len(self.bar_values)):
            current = self.bar_values[i]
            j = i - 1
            while j >= 0 and self.bar_values[j] > current:
                self.bar_values[j + 1] = self.bar_values[j]
                self.draw_bar(j + 1, self.bar_values[j + 1], BAR_ACTIVE)
                yield
                self.draw_bar(j + 1, self.bar_values[j + 1], BAR_COLOR)
                j -= 1
            self.bar_values[j + 1] = current
            self.draw_bar(j + 1, current, BAR_ACTIVE)
            yield
            self.draw_bar(j + 1, current, BAR_COLOR)
        self.color_all_bars(BAR_DONE)

# Merge sort
    def merge_sort(self):
        """
    Generator implementation of merge sort using recursion.
    """
        yield from self.merge_sort_helper(0, len(self.bar_values) - 1)
        self.color_all_bars(BAR_DONE)

    def merge_sort_helper(self,left, right):
        if left < right:
            middle = (left + right) // 2
            yield from self.merge_sort_helper(left, middle)
            yield from self.merge_sort_helper(middle + 1, right)
            yield from self.merge_subarrays(left, middle, right)

    def merge_subarrays(self,left, mid, right):
        left_part = self.bar_values[left:mid+1]
        right_part = self.bar_values[mid+1:right+1]

        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                self.bar_values[k] = left_part[i]
                i += 1
            else:
                self.bar_values[k] = right_part[j]
                j += 1
            self.draw_bar(k, self.bar_values[k], BAR_ACTIVE)
            yield
            self.draw_bar(k, self.bar_values[k], BAR_COLOR)
            k += 1

        while i < len(left_part):
            self.bar_values[k] = left_part[i]
            self.draw_bar(k, self.bar_values[k], BAR_ACTIVE)
            yield
            self.draw_bar(k, self.bar_values[k], BAR_COLOR)
            i += 1
            k += 1

        while j < len(right_part):
            self.bar_values[k] = right_part[j]
            self.draw_bar(k, self.bar_values[k], BAR_ACTIVE)
            yield
            self.draw_bar(k, self.bar_values[k], BAR_COLOR)
            j += 1
            k += 1

    def quick_sort(self):
        """
    Generator implementation of quick sort using a pivot
    and recursive partitioning.
    """
        yield from self.quick_sort_helper(0, len(self.bar_values) - 1)
        self.color_all_bars(BAR_DONE)

    def quick_sort_helper(self,low, high):
        if low < high:
            pivot_index = yield from self.partition(low, high)
            yield from self.quick_sort_helper(low, pivot_index - 1)
            yield from self.quick_sort_helper(pivot_index + 1, high)

    def partition(self,low, high):
        pivot_val = self.bar_values[high]
        i = low
        for j in range(low, high):
            if self.bar_values[j] <= pivot_val:
                self.bar_values[i], self.bar_values[j] = self.bar_values[j], self.bar_values[i]
                self.draw_bar(i, self.bar_values[i], BAR_ACTIVE)
                self.draw_bar(j, self.bar_values[j], BAR_ACTIVE)
                yield
                self.draw_bar(i, self.bar_values[i], BAR_COLOR)
                self.draw_bar(j, self.bar_values[j], BAR_COLOR)
                i += 1

        self.bar_values[i], self.bar_values[high] = self.bar_values[high], self.bar_values[i]
        self.draw_bar(i, self.bar_values[i], BAR_ACTIVE)
        self.draw_bar(high, self.bar_values[high], BAR_ACTIVE)
        yield
        self.draw_bar(i, self.bar_values[i], BAR_COLOR)
        self.draw_bar(high, self.bar_values[high], BAR_COLOR)
        return i

    def heap_sort(self):
        """
    Generator implementation of heap sort using a max heap.
    """
        n = len(self.bar_values)

        #the heap
        for i in range(n // 2 - 1, -1, -1):
            yield from self.heapify(n, i)

    # Extracting elements one by one
        for end in range(n - 1, 0, -1):
            self.bar_values[0], self.bar_values[end] = self.bar_values[end], self.bar_values[0]
            self.draw_bar(0, self.bar_values[0], BAR_ACTIVE)
            self.draw_bar(end, self.bar_values[end], BAR_ACTIVE)
            yield
            self.draw_bar(0, self.bar_values[0], BAR_COLOR)
            self.draw_bar(end, self.bar_values[end], BAR_COLOR)
            yield from self.heapify(end, 0)

        self.color_all_bars(BAR_DONE)

    def heapify(self,size, root):
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < size and self.bar_values[left] > self.bar_values[largest]:
            largest = left
        if right < size and self.bar_values[right] > self.bar_values[largest]:
            largest = right

        if largest != root:
            self.bar_values[root], self.bar_values[largest] = self.bar_values[largest], self.bar_values[root]
            self.draw_bar(root, self.bar_values[root], BAR_ACTIVE)
            self.draw_bar(largest, self.bar_values[largest], BAR_ACTIVE)
            yield
            self.draw_bar(root, self.bar_values[root], BAR_COLOR)
            self.draw_bar(largest, self.bar_values[largest], BAR_COLOR)
            yield from self.heapify(size, largest)

#sorting animation
    def begin_sort(self):
        """
    Starts the selected sorting algorithm and initializes
    the animation process.
    """
        self.sort_process=None
        self.color_all_bars(BAR_COLOR)
        selected = self.algorithm_choice.get()

        if selected == "Insertion Sort":
            self.sort_process = self.insertion_sort()
        elif selected == "Merge Sort":
            self.sort_process = self.merge_sort()
        elif selected == "Quick Sort":
            self.sort_process = self.quick_sort()
        else:
            self.sort_process = self.heap_sort()

        self.animate_step()

    def animate_step(self):
        """
    Advances the sorting animation by one step using the
    generator and schedules the next step.
    """
        if self.sort_process:
            try:
                next(self.sort_process)
                self.root.after(self.speed_slider.get(), self.animate_step)
            except StopIteration:
                self.sort_process = None

#bars with randomized values
    def reset_bars(self):
        """
    Generates a new random dataset and redraws all bars.
    Also resets any running sorting process.
    """
        self.sort_process = None
        self.canvas.delete("all")
        self.bars = []
        self.bar_values = []

        num_bars = self.size_slider.get()
        self.bar_width = WIDTH // num_bars
        data = list(range(1, num_bars + 1))
        random.shuffle(data)

        for i, val in enumerate(data):
            height = val * (HEIGHT // num_bars)  #scaling factor
            self.bar_values.append(height)
            self.bars.append(self.canvas.create_rectangle(0, 0, 0, 0, fill=BAR_COLOR))
            self.draw_bar(i, height, BAR_COLOR)
        
SortingVisualizer()    