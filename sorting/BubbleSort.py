'''
Created on 15-Nov-2016

@author: kiran
'''

def bubbleSort(arr):
    n = len(arr)
    flag = 1
    # Traverse through all array elements
    #for i in range(n):
    while(flag):
        flag = 0
        # Last i elements are already in place
        for j in range(0, n-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
                flag = 1
 
# Driver code to test above
arr = [64, 34, 25, 12, 22, 11, 90]
 
bubbleSort(arr)
 
print ("Sorted array is:")
for i in range(len(arr)):
    #prints array elements in different lines
    print ("%d" %arr[i]),
    #prints array elements in same line
    print ("%d " %arr[i],end='')
