def a3():
    print('''


import numpy as np

step_function = lambda x: 1 if x >= 0 else 0
training_data = []

def to_binarylist(asci):
    return np.array([int(x) for x in list('{0:06b}'.format(asci))])

for asci in range(ord('0'),ord('9')+1):
    training_data.append({'input':to_binarylist(asci),'label': 1 if(asci%2==0) else 0})

weights = np.array([0, 0, 0, 0, 0, 1])

for data in training_data:
    inp=data['input']
    label = data['label']
    output = step_function(np.dot(inp, weights))
    error = label - output
    weights += inp * error

number = input("Enter a Number (0-9): ")
binary = to_binarylist(ord(number))
output = "even" if step_function(np.dot(binary, weights)) == 1 else "odd"
print(number, " is ", output)''')
a3()