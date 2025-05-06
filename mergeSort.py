import random
import time

# Merge sort algorithm that can sort by a key
def merge_sort(arr, key_index=None):
    """
    Sort the array using merge sort algorithm.
    
    Args:
        arr: List to be sorted
        key_index: Optional index for sorting lists of lists/tuples by a specific element
                   If None, sorts the elements directly
    """
    if len(arr) <= 1:
        return arr
        
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    # Recursively apply merge sort on both halves
    merge_sort(left_half, key_index)
    merge_sort(right_half, key_index)
    
    # Merge the two sorted halves
    i = j = k = 0
    while i < len(left_half) and j < len(right_half):
        # Compare by key index if provided
        if key_index is not None:
            left_val = left_half[i][key_index] if left_half[i][key_index] is not None else ""
            right_val = right_half[j][key_index] if right_half[j][key_index] is not None else ""
            if str(left_val).lower() <= str(right_val).lower():
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
        else:
            # Direct comparison
            if left_half[i] <= right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
        k += 1
    
    # Add remaining elements from left_half
    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1
    
    # Add remaining elements from right_half
    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1
    
    return arr

# Test the merge sort implementation when run directly
if __name__ == "__main__":
    # User input to generate random numbers
    num_elements = int(input("Enter the number of elements to be generated in the array: "))
    
    # Generate a list of random integers between 1 and 100
    arr = [random.randint(1, 100) for _ in range(num_elements)]
    print(f"\nGenerated random array: {arr}")
    
    user_response = input("\nDo you want to run Merge sort now? (yes/no): ").strip().lower()
    
    if user_response == 'yes':
        # Measure execution time for merge sort
        start_time = time.time()
        merge_sort(arr)
        end_time = time.time()
        
        # Display the results
        print(f"\nSorted array: {arr}")
        print(f"Execution time: {end_time - start_time:.6f} seconds")