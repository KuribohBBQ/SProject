import random
from collections import deque
from models import Professor, Student
from dataclasses import dataclass, field
from typing import List, Optional
import time

def match(students: List[Student], professors: List[Professor]):
    """
    -parameters are a list of students and professors to match
    -for each student, use duckdb to get a list of professors from parquet file ordered by compatibility score descending
    -start with the top professor in the list
        -if professor has open slots, pair that student with the professor
            Student.pairedwith = Professor
            Professor.currentpositions[k] = Student
        -else if professor has no slots open, go through each student in their list
            -compare compatibility score with current student with compatibility of accepted student
                -if current student has higher compatibility than accepted student
                    -replace the accepted student with current student in the professor's list
                -else move on to the next professor
    """
    #run time
    start= time.time()

    #list of students that need to be paired
    students_to_be_paired = students



