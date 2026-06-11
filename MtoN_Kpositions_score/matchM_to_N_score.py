from collections import deque
from typing import List
import time

from models import Professor, Student
from calc_compatibility import calculate_compatibility
from generate import generate_random_instance


def match(students: List[Student], professors: List[Professor]):
    start = time.time()

    
    #preference list to hold stability score for each student has for each professor
    prefs = {}

    for student in students:
        scored_professors = []

        for professor in professors:
            score = calculate_compatibility(
                studentscores=student.interest_score_list,
                professorscores=professor.interest_score_list
            )

            scored_professors.append((professor, float(score)))

        scored_professors.sort(key=lambda x: x[1], reverse=True)
        prefs[student.emplID] = scored_professors

    
    #deque to create a list of students to match
    students_to_be_matched = deque(students)

    #index for the next professor that a student will ask. Each student has their own index that starts at 0
    #student will ask professor at index 0, then when they have to ask the next professor, they will ask professor at index 1, and so on
    next_professor = {
        student.emplID: 0 for student in students
    }
    
    #begin loopping
    while students_to_be_matched:
        potential_student = students_to_be_matched.popleft()

        #skip if student already proposed to everyone
        if next_professor[potential_student.emplID] >= len(professors):
            continue

        #get student's next-best professor
        prof_list = prefs[potential_student.emplID]
        potential_professor, potential_score = prof_list[next_professor[potential_student.emplID]]
        next_professor[potential_student.emplID] += 1

        #ff professor has open slot, ao accept student
        if potential_professor.positions_open > 0:
            potential_student.pairedwith = (potential_professor, potential_score)

            #add the student to the next open slot in the professor's position list
            for i in range(len(potential_professor.currentpositions)):
                if potential_professor.currentpositions[i] is None:
                    potential_professor.currentpositions[i] = (potential_student, potential_score)
                    break

            #professor now has 1 less spot open
            potential_professor.positions_open -= 1

            #if professor has 0 open slots, they are now closed
            if potential_professor.positions_open == 0:
                potential_professor.open = False

        else:
            #professor is full, so find currently assigned student with lowest score
            worst_index = None
            worst_student = None
            #any score will be lower than infinity
            worst_score = float("inf")

            for i, entry in enumerate(potential_professor.currentpositions):
                assigned_student, assigned_score = entry

                if assigned_score < worst_score:
                    worst_score = assigned_score
                    worst_student = assigned_student
                    worst_index = i

            #professor prefers new student over their current worst student
            if potential_score > worst_score:
                worst_student.pairedwith = None

                potential_professor.currentpositions[worst_index] = (
                    potential_student,
                    potential_score
                )

                potential_student.pairedwith = (
                    potential_professor,
                    potential_score
                )

                #rejected student continues proposing
                if next_professor[worst_student.emplID] < len(professors):
                    students_to_be_matched.append(worst_student)

            else:
                #professor rejects student; student tries next professor
                if next_professor[potential_student.emplID] < len(professors):
                    students_to_be_matched.append(potential_student)

    end = time.time()
    print(f"Total runtime of the program is {end - start} seconds")

    for s in students:
        if s.pairedwith is not None:
            print(f"{s.name} will work with {s.pairedwith[0].name}")
        else:
            print(f"{s.name} is paired with no one")

    print("\n--- Professor Assignments ---")
    for p in professors:
        print(f"{p.name}:")

        has_students = False
        for entry in p.currentpositions:
            if entry is not None:
                student, score = entry
                print(f"  - {student.name} (score: {score:.3f})")
                has_students = True

        if not has_students:
            print("  - No students assigned")

if __name__ == "__main__":

    students, professors = generate_random_instance()
    match(students, professors)

           

            


            
        







        

    
  




