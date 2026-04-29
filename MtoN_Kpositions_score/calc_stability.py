import random
from collections import deque
import sys
import numpy as np

def calculate_stability(studentscores: list, professorscores: list):
    if len(studentscores) != len(professorscores):
        print("Error. Student and professor do not share same list length")
        sys.exit()

    #convert lists to array for dot product
    student_array = np.array(studentscores, dtype=float)
    professor_array = np.array(professorscores, dtype=float)

    #normalize student and professor array
    normal_student = student_array / np.linalg.norm(student_array)
    normal_professor = professor_array / np.linalg.norm(professor_array)

    #return the dot product
    return np.dot(normal_student, normal_professor)

    
    

