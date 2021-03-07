import random
import numpy as np
"""
Redundancy Rate
"""
rate = 0.2          # Redundancy Rate
all_order = []      # List of problems that were used for all trainees

trainees = 10       # Number of trainees
num_questions = 5   # Number of problems for each trainee

problems = list(range(1, 100))      # Imitation of existed a list of problems
length = len(problems)              # Count of problems
print("Length:", length)

iterations = np.around(trainees * rate)     # Define how many problems can be the same for different trainees
it = iterations

print("Iterations:", iterations)
print()

# Loop for Trainees
for t in range(trainees):
    # To break the loop if number of problems are not enough for trainees (repeating problems are limited)
    if len(problems)+it < trainees*num_questions:
        break
    order = []  # List of problems for only one trainee

    # Loop stop when will find defined number of problems
    while len(order) != num_questions:
        p = random.choice(problems)     # get random problem from the list (can be the same problems)

        # To add a new problem to list if the number of the same problems not higher then redundancy rate (iterations)
        if order.count(p) == 0 and all_order.count(p) <= iterations:
            order.append(p)
            all_order.append(p)     # before all_order.count(p) = 0 after append = 1

            # To subtract the number of iterations if the problem were already used
            if all_order.count(p) != 1 and iterations >= 1:     # all_order.count(p) = 1
                print("Used question:", p)
                iterations -= 1
        else:
            continue

    print(order)
print(all_order)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////

"""
Course Distributions
"""
questions = 10        # Number of Questions
list_problems = []

course_1 = list(range(1, 20))
course_2 = list(range(20, 40))
course_3 = list(range(40, 60))
course_4 = list(range(60, 80))
course_5 = list(range(80, 100))

courses = [course_1, course_2, course_3, course_4, course_5]
weights = [60, 5, 5, 5, 30]     # Weights in percentages

while len(list_problems) != questions:
    # Choose list of problems from random (with weights) course
    course = random.choices(courses, weights=weights, k=1)[0]

    p = random.choice(course)   # Choose a random problem from course

    if list_problems.count(p) == 0:     # if we didn't use that problem then we will add to list
        list_problems.append(p)         # List of problems with course distributions

print()
print(list_problems)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////

"""
Level Distribution
"""

questions = 10        # Number of Questions
list_problems = []

level_1 = list(range(1, 10))
level_2 = list(range(10, 20))
level_3 = list(range(20, 30))
level_4 = list(range(30, 40))
level_5 = list(range(40, 50))

levels = [level_1, level_2, level_3, level_4, level_5]

# Prepare weights in percentages
LOW = 10
LOW_MEDIUM = 20
MEDIUM = 40
MEDIUM_HIGH = 20
HIGH = 10
weights = [LOW, LOW_MEDIUM, MEDIUM, MEDIUM_HIGH, HIGH]

while len(list_problems) != questions:
    # Choose list of problems from random (with weights) levels
    level = random.choices(levels, weights=weights, k=1)[0]
    print(level)

    p = random.choice(level)   # Choose a random problem from level
    print(p)

    if list_problems.count(p) == 0:     # if we didn't use that problem then we will add to list
        list_problems.append(p)         # List of problems with level distributions

print()
print(list_problems)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////

# To add to problem class (testings)

# order = []
# all_order = []
# rate = 0.2          # Redundancy Rate
# trainees = 10       # Number of trainees
#
# problems = list(range(1, 100))      # Imitation of existed a list of problems
# length = len(problems)              # Count of problems
# iterations = np.around(trainees * rate)
#
#
# while True:
#     p = random.choice(problems)
#     if order.count(p) == 0 and all_order.count(p) <= iterations:
#         order.append(p)
#         all_order.append(p)
#
#         if all_order.count(p) != 1 and iterations >= 1:
#             print("Used question:", p)
#             iterations -= 1
#         break
#     else:
#         continue
#
# print(order[-1])
# print(all_order[-1])
