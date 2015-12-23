import numpy as np 
import matplotlib.pyplot as plt

def fibonacci (n):
	f_0 = 0
	f_1 = 1
	seq = [f_0, f_1]
	curr = 0 
	l1 = f_0
	l2 = f_1
	i = 2 
	while i < n:
		curr = l1 + l2
		seq.append (curr)
		l1 = seq[i - 1]
		l2 = curr 
		i += 1

	return seq

# Weight vector based on Fibonacci sequence
def portion (seq, stateNum):
	# if stateNum >= 10:
	# 	stateNum = 9
	weight  = [] 
	start_idx = stateNum * 2 + 1 
	curr_idx = start_idx
	dom = seq[start_idx + 1]
	numTerms = stateNum + 1 
	while numTerms != 0:
		weight.append (float(seq[curr_idx]))
		curr_idx -= 2
		numTerms -= 1

	return np.divide (weight, dom)

# Generate randon walk data
def random_walk (size):
	wn = np.random.randn (size, 1)
	rw = [wn[0][0]] 
	curr_idx = 1 
	while curr_idx < size: 
		rw.append ((rw[curr_idx - 1] + wn[curr_idx])[0])
		curr_idx += 1

	return rw

# Given current state, random walk, and weight vector, estimate next state
def estimate (port, rw, stateNum):
	port_sec = np.array (port)
	rw_sec = np.array(rw[:stateNum + 1])
	rw_sec = np.array(list(reversed (rw_sec)))
	est = np.dot(port_sec,rw_sec.T)
	return est

# Plot
def plot (filtered, rw):
	x = range (1, len (filtered) + 1) 
	plt.plot (x, filtered, color='r') 
	plt.plot (x, rw, color='b') 
	plt.xlabel('Time') 
	plt.ylabel('Value') 
	plt.show()

# Simple recursive kalman filter
def kfilter (rw, numStates, seq):
	i = 0 
	filtered = [] 
	while i < numStates:
		port = portion (seq, i)
		filtered.append (estimate (port, rw, i))
		i+=1

	return filtered

# Calculate mean square error
def calculate_mse (filtered, rw):
	diff_list = np.square(np.subtract(filtered, rw))
	mse = float(sum (diff_list)) / float(len (diff_list))
	print ("The mean squared error is ", mse)
	return mse


if __name__ == '__main__':
	numStates = 500
	seq = fibonacci (2000)
	rw = random_walk (numStates)
	filtered = kfilter (rw, numStates, seq) 
	calculate_mse (filtered, rw)
    plot (filtered, rw)
