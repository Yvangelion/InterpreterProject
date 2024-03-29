# inputs
inputs = [
    (-1, -1, -1, -1),  
    (-1, -1, -1, 1),   
    (-1, -1, 1, -1),   
    (-1, -1, 1, 1),    
    (-1, 1, -1, -1),   
    (-1, 1, -1, 1),   
    (-1, 1, 1, -1),    
    (-1, 1, 1, 1),     
    (1, -1, -1, -1),   
    (1, -1, -1, 1),    
    (1, -1, 1, -1),    
    (1, -1, 1, 1),     
    (1, 1, -1, -1),   
    (1, 1, -1, 1),     
    (1, 1, 1, -1),     
    (1, 1, 1, 1)       
]
#targets = [1, 0, 0, 0] # and 
#targets = [0, 1, 1, 1] # or 
targets = [1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1]
w0 = -0.5
w1 = 0.7
w2 = -0.2
w3 = 0.1
w4 = 0.9
learning_rate = 0.1
epochs = 10000

def calculate_sum(x1, x2, x3, x4, w1, w2, w3, w4, w0):
    # could do x1 = 1 and w0 updates
    return x1 * w1 + x2 * w2 + x3 * w3 + x4 * w4 + w0


def step_function(sum_val): #architecture of the perceptron 
    if sum_val > 0:
        return 1
    elif sum_val <= 0:
        return -1
    #return 1 if sum_val > 0 else 0

def update_weights(w1, w2, w3, w4, x1, x2, x3, x4, target, output, learning_rate):
    delta = learning_rate * (target - output)  # Compute delta (delta(i))
    # i am keeping delta0 and w0 as constant
    delta1 = delta * x1  
    delta2 = delta * x2  
    delta3 = delta * x3 
    delta4 = delta * x4  

    w1 += delta1
    w2 += delta2
    w3 += delta3
    w4 += delta4

    w1 = round(w1, 1)
    w2 = round(w2, 1)
    w3 = round(w3, 1)
    w4 = round(w4, 1)

    return w1, w2, w3, w4, delta1, delta2, delta3, delta4



#training
for epoch in range(epochs):# each iteration of epochs
    c = epoch + 1
    num = 1 
           
    print(f"\nEpoch {c}:")# building table
    print("Sample\tInput (x1, x2)\tTarget (y)\tWeights (w1, w2)\tS\tOutput (o)\tError\tDelta1\tDelta2\tUpdated Weights (w1, w2)")
    for sample, target in zip(inputs, targets):
        x1, x2, x3, x4 = sample  # Unpack all four elements of the input sample
        s = calculate_sum(x1, x2, x3, x4, w1, w2, w3, w4, w0)  # Update the sum calculation
        output = step_function(s)
        error = target - output
        w1_prev, w2_prev, w3_prev, w4_prev = w1, w2, w3, w4  # Update the previous weights

        print(f"{num}\t{sample}\t\t{target}\t\t({w1}, {w2}, {w3}, {w4})\t\t{s:.1f}\t{output}\t\t{error}\t", end="")
        if error != 0:
            w1, w2, w3, w4, delta1, delta2, delta3, delta4 = update_weights(w1, w2, w3, w4, x1, x2, x3, x4, target, output, learning_rate)
            print(f"{delta1:.1f}\t{delta2:.1f}\t{delta3:.1f}\t{delta4:.1f}\t({w1}, {w2}, {w3}, {w4})")
        else:
            print("0.0\t0.0\t0.0\t0.0\t", end="")
            print(f"({w1}, {w2}, {w3}, {w4})")
        num += 1

