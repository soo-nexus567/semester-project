#flights would be a dictionary with key value pairs for author,
def merge_sort(flights, sortOption):
    if len(flights) > 1:
        mid = len(flights) // 2 # Find the middle index
        left_half = flights[:mid] #Divide list into halves
        right_half = flights[mid:]
        merge_sort(left_half)
        merge_sort(right_half)
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if len(left_half[i][0]) == len(right_half[j][0]) and left_half[i][1][1] < right_half[j][1][1]:                
                    # if left_half[i][1][1] < right_half[j][1][1]:
                flights[k] = left_half[i]
                i += 1
            else:
                flights[k] = right_half[j]
                j += 1
                k += 1
        while i < len(left_half):
            flights[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            flights[k] = right_half[j]
            j += 1
            k += 1
# Take user input
books = [
    ["To Kill a Mockingbird", ["Harper Lee", 1960]],
    ["1984", ["George Orwell", 1949]],
    ["Pride and Prejudice", ["Jane Austen", 1813]],
    ["The Great Gatsby", ["F. Scott Fitzgerald", 1925]],
    ["Moby Dick", ["Herman Melville", 1851]]
]

merge_sort(books)
print(books)
print()
print(sorted(books, key=lambda x: x[0]))