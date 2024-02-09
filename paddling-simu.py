# This program will tell you how you should distribute your power over a course (both time-wise and distance-wise) in order to finish as quickly as possible.
# 	Right-hand Reimann sums are used.
# Known constants: drag coefficient D, boat mass M, maximum paddler energy E
# Known equations: net foce = M*a, drag equation, F*d = E, tfinish = minimum possible
# Unknown: the Fpaddler(x) curve and the Fpaddler(t) curve

import pickle

# Step 1: Every possible curve of Fpaddler(x) is found. Those with integrals E will be used.
	# note: a "resolution" value of 8 here makes Step 1 take about 30s to compute. However, if you can store all the possible points_list's that give passing graphs somewhere in a file, then you'll only have to run Step 1 once.
resolution = eval(input("\nType resolution (6 recommended for testing, 11 for simulation): ")) # our graph is made on a grid of possible points with this resolution. Note that the graph's axes are bounded as: ([0,resolution],[0,resolution]), but the points will max out at values of resolution-1 actually.
user_input = input("\nType 'y' to do step 1 again, or type 'n' to use the pickled data from prev run:  ")
if user_input == "y":
	points_list = [] #This will be the y values that our graph has
	winning_lists = [] #This will be a list, where I'll store the winning lists that produce graphs with the correct amount of area under the curve
	E_value = resolution**2 * int(0.3*resolution)/resolution   #note: we have to find out what curves have the right amount of graph area (ie 1/3 of the graph). But I don't wanna measure the graph area as a decimal for fear of float rounding errors. So, I'll imagine the graph as a grid and simply count boxes in it, as a whole number. If a graph has this correct amount of boxes under its curve (or really, Reimann sum), then it passes.
	for count in range(0,resolution): #make it an empty list with the correct length
		points_list = points_list + [0]
	# Test the current list to see if it equals E (which I'm gonna arbitrarily set to equal "" as the fraction of total graph area, ie 1/4 of the total graph area for resolution=8). And iterates through all possible lists
	not_done_yet = True
	while not_done_yet:
		# We are now testing a new combo of points_list. Ie, if the prev iteration was [0,3,4,3,1] , we're now at [0,3,4,3,2] (obviously this example has resolution = 5, thus each item has a max value of 4)
		# print("\nNow we have:",points_list)
		# unused_var = input()
		if sum(points_list) == E_value:
			# print("Graph passes\n") #This list of points has the desired area under the curve
			print("Graph passes:",points_list)
			winning_lists.append(points_list[:]) #The "[:]" is necessary for winning_lists to be correct, but how Python works in that way I have no idea.
			#print(winning_lists)
		# Now we will prepare the next iteration
		points_list[-1] = points_list[-1] + 1
		# Check that we didn't just overflow that least-significant digit. And if so, carry it over to the next place. Check that next place to make sure it doesn't also overflow.
		for count in range(resolution-1,-1,-1): #count will be used to index points_list for the item we're currently looking at
			# print("\ntrying to increase list at index",count)
			if points_list[count] == resolution: #note that "resolution" is also equal to the limit slash overflow value an item in the list can have
				if count != 0 : 
					points_list[count-1] = points_list[count-1] + 1 #carrying over the one essentially
					points_list[count] = 0 
				else: # when we get here, it means that points_list[0] has overflowed (as in, it's equal to "resolution" now) and we can stop the while loop
					not_done_yet = False		
			else: #This means the current digit didn't overflow as it increased. So, obviously the next (more significant) digits won't overflow either, and we don't have to check them.
				break
	print("\nAll possible graphs tested. Of all" , resolution**resolution , "possibilities tested," , len(winning_lists) , "were successful. They are:")
	unused_variable = input()
	
	# Pickle winning_lists now
	open('Step1.pickle', 'w').close() # delete the contents of the storage file if it even exists
	my_file = open('Step1.pickle', 'wb') # open the file
	pickle.dump(winning_lists, my_file)
	my_file.close()
else: #note that your pickled data must have been made with the same "resolution" that you're using in this current run of the program, or else you'll get errors
	my_file = open('Step1.pickle', 'rb')
	winning_lists = pickle.load(my_file)
	my_file.close()

print(winning_lists)

# Step 2: Now, calculus will be done to find which curve of paddler force applied over the distance of the race, will produce the fastest trial time for the paddler.
	