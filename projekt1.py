import sys
import random
sys.setrecursionlimit(10**6)



def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def shell_sort(arr):
    l = [1]
    n = len(arr)
    k = 0 
    gap = 1
    while gap < n:
        gap = 4**(k+1)+3*(2**k)+1
        if gap <= n:
            l.append(gap)
        k += 1
    l = l[::-1]
    for gap in l:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] < temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp

def selection_sort(arr):
    for i in range(len(arr)):
        min_index = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[i] < arr[l]:
        largest = l
    if r < n and arr[largest] < arr[r]:
        largest = r 
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest) 
def heap_sort(arr):
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

def partition(arr, low, high):
    pivot = arr[low]
    left = low + 1
    right = high
    done = False
    while not done:
        while left <= right and arr[left] <= pivot:
            left = left + 1
        while arr[right] >= pivot and right >= left:
            right = right -1
        if right < left:
            done = True
        else:
            arr[left], arr[right] = arr[right], arr[left]
    arr[low], arr[right] = arr[right], arr[low]
    return right

def quicksort_left_pivot(arr, low, high):
    if low < high:
        pivot = partition(arr, low, high)
        quicksort_left_pivot(arr, low, pivot - 1)
        quicksort_left_pivot(arr, pivot + 1, high)

def partition_random(arr, low, high):
    pivot_index = random.randint(low, high)
    pivot = arr[pivot_index]
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort_random_pivot(arr, low, high):
    if low < high:
        pivot_index = partition_random(arr, low, high)
        quick_sort_random_pivot(arr, low, pivot_index - 1)
        quick_sort_random_pivot(arr, pivot_index + 1, high)

def sort_using_algorithm(data, algorithm):
    if algorithm == 1:
        insertion_sort(data)
    elif algorithm == 2:
        shell_sort(data)
    elif algorithm == 3:
        selection_sort(data)
    elif algorithm == 4:
        heap_sort(data)
    elif algorithm == 5:
        quicksort_left_pivot(data, 0, len(data) - 1)  
    elif algorithm == 6: 
        quick_sort_random_pivot(data, 0, len(data) - 1)  

    return data


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--algorithm":
        print("Usage: python script.py --algorithm <algorithm_number>")
        sys.exit(1)

    algorithm_number = int(sys.argv[2])

    try:
        data = [int(x) for x in sys.stdin.read().split()]
    except EOFError:
        print("Error reading input.")

    sorted_data = sort_using_algorithm(data[1::], algorithm_number)

    print("Sorted data:", sorted_data[:10])

if __name__ == "__main__":
    main()
