import pytest

def selectionSort(array):
  """
  A function that takes an array de integers and return a sorted version 
  of that array using Selection Sort Algorithm. 
  """
  currentIdx = 0
  while currentIdx < len(array) - 1:
      smallestIdx = currentIdx
      for i in range(currentIdx + 1, len(array)):
          if array[smallestIdx] > array[i]:
              smallestIdx = i
      swap(currentIdx, smallestIdx, array)
      currentIdx += 1
  return array

def swap(i, j, array):
  """
  Swap the items i, j of array
  """
  array[i], array[j] = array[j], array[i]

@pytest.fixture(scope="session")
def data():
    
    array = []
    
    # test 1 data
    array.append([8, 5, 2, 9, 5, 6, 3])

    # test 2 data
    array.append([1])

    # test 3 data
    array.append([1, 2])

    # test 4 data
    array.append([2, 1])

    # test 5 data
    array.append([-4, 5, 10, 8, -10, -6, -4, -2, -5, 3, 5, -4, -5, -1, 1, 6, -7, -6, -7, 8])

    # test 6 data
    array.append([-7, 2, 3, 8, -10, 4, -6, -10, -2, -7, 10, 5, 2, 9, -9, -5, 3, 8])

    # test 7 data
    array.append([544, -578, 556, 713, -655, -359, -810, -731, 194, -531, -685, 689, -279, -738, 886, -54, -320, -500, 738, 445, -401, 993, -753, 329, -396, -924, -975, 376, 748, -356, 972, 459, 399, 669, -488, 568, -702, 551, 763, -90, -249, -45, 452, -917, 394, 195, -877, 153, 153, 788, 844, 867, 266, -739, 904, -154, -947, 464, 343, -312, 150, -656, 528, 61, 94, -581])
    
    return array

def test_1(data):
    """
    Test evaluation for [8, 5, 2, 9, 5, 6, 3]
    """
    assert selectionSort(data[0]) == [2, 3, 5, 5, 6, 8, 9]

def test_2(data):
    """
    Test evaluation for [1] 
    """
    assert selectionSort(data[1]) == [1]

def test_3(data):
    """
    Test evaluation for [1,2]
    """
    assert selectionSort(data[2]) == [1,2]

def test_4(data):
    """
    Test evaluation for [2,1]
    """
    assert selectionSort(data[3]) == [1,2]

def test_5(data):
    """
    Test evaluation for [-4, 5, 10, 8, -10, -6, -4, -2, -5, 3, 5, -4, -5, -1, 1, 6, -7, -6, -7, 8] 
    """
    assert selectionSort(data[4]) == [-10, -7, -7, -6, -6, -5, -5, -4, -4, -4, -2, -1, 1, 3, 5, 5, 6, 8, 8, 10] 

def test_6(data):
    """
    Test evaluation for [-7, 2, 3, 8, -10, 4, -6, -10, -2, -7, 10, 5, 2, 9, -9, -5, 3, 8]
    """
    assert selectionSort(data[5]) == [-10, -10, -9, -7, -7, -6, -5, -2, 2, 2, 3, 3, 4, 5, 8, 8, 9, 10]

def test_7(data):
    """
    Test evaluation for [544, -578, 556, 713, -655, -359, -810, -731, 194, -531, -685, 689, -279, -738, 886, -54, -320, -500, 738, 445, -401, 993, -753, 329, -396, -924, -975, 376, 748, -356, 972, 459, 399, 669, -488, 568, -702, 551, 763, -90, -249, -45, 452, -917, 394, 195, -877, 153, 153, 788, 844, 867, 266, -739, 904, -154, -947, 464, 343, -312, 150, -656, 528, 61, 94, -581]
    """
    assert selectionSort(data[6]) == [-975, -947, -924, -917, -877, -810, -753, -739, -738, -731, -702, -685, -656, -655, -581, -578, -531, -500, -488, -401, -396, -359, -356, -320, -312, -279, -249, -154, -90, -54, -45, 61, 94, 150, 153, 153, 194, 195, 266, 329, 343, 376, 394, 399, 445, 452, 459, 464, 528, 544, 551, 556, 568, 669, 689, 713, 738, 748, 763, 788, 844, 867, 886, 904, 972, 993]
