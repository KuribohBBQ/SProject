import random
from collections import deque
from models import Professor, Student
from dataclasses import dataclass, field
from typing import List, Optional
import time
import duckdb as db
from generate import generate_random_instance
from process_parquet import convert_to_parquet
from readparquet import fetch_sorted_results, pretty_print_results, load_preferences


def fetch_row(professorName: str, x: int):
    con = db.connect()
    result = con.execute("""
        SELECT *
        FROM read_parquet('matches.parquet')
        WHERE professorName = ?
        ORDER BY stabilityScore DESC
        LIMIT 1 OFFSET ?
    """, [professorName, x]).fetchone()
    con.close()

    return result



def match(students: List[Student], professors: List[Professor]):
    """
    -parameters are a list of students and professors to match
    -for each professor, use duckdb to get a list of students from parquet file ordered by compatibility score descending
    -start with the top student in the list
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


    student_lookup = {student.emplID: student for student in students}

    prefs = load_preferences("matches.parquet")
    

    #list of students that need to be paired
    professors_to_be_matched = deque(professors)

    #index for the next professor that the student will work with 
    nextStudent = {}
    for professor in professors:
        #each professor will start off at index 0. 0 means they will start at checking the student with the highest score in the list
        nextStudent[professor.name] = 0

    #infinite while loop until there are no more students to pair
    while professors_to_be_matched:

        #pop professor from list
        potential_professor = professors_to_be_matched.popleft()

        #if professor has already asked everyone in the student list, skip them
        if nextStudent[potential_professor.name] >= len(students):
            continue

        #if professor already has all their slots filled, skip them
        if potential_professor.open is False:
            continue


        
        #variable to fetch the xth row in the parquet file
        fetch_xth_row = nextStudent[potential_professor.name]
        #returns row_data[0] = studentName, row_data[1] = emplID, row_data[2] = professorName, row_data[3] = stabilityScore
        prof_list = prefs[potential_professor.name]

        if fetch_xth_row >= len(prof_list):
            continue

        row_data = prof_list[fetch_xth_row]
        #add 1 to the index of the professor
        nextStudent[potential_professor.name] += 1

        #if row data is none, then there are no more students to go through
        if row_data is None:
            continue

        #get potential student through row_data's emplID
        potential_student = student_lookup.get(row_data[1])

        if potential_student is None:
            continue

        #the compatibility score of potential professor with potential student
        potential_prof_score = row_data[2]

       #if potential student is paired with no one, add student to the current professor's open slots
        if potential_student.pairedwith is None:
            potential_student.pairedwith = (potential_professor, potential_prof_score)

            #add the student to the professors open slots
            for i in range(len(potential_professor.currentpositions)):
                if potential_professor.currentpositions[i] is None:
                    potential_professor.currentpositions[i] = (potential_student, potential_prof_score)
                    break
            
            #subtract 1 from the professors open positions
            potential_professor.positions_open -= 1

            #if all positions are now filled, make field open False
            if potential_professor.positions_open == 0:
                potential_professor.open = False
            #else add them back
            else:
                professors_to_be_matched.append(potential_professor)
        
        #else if the potential student is already matched with a professor, check if current professor has lower compatibility score
        else:
            current_prof, current_prof_score = potential_student.pairedwith
            if potential_prof_score > current_prof_score:
                #if true, then the potential student is better working with potential professor, so make potential professor the new pairing

                # remove student from old professor
                for i, entry in enumerate(current_prof.currentpositions):
                    if entry is not None and entry[0] == potential_student:
                        current_prof.currentpositions[i] = None
                        current_prof.positions_open += 1
                        current_prof.open = True
                        #and since old professor has open slots again, put them back into the list
                        professors_to_be_matched.append(current_prof)
                        break

                #add potential student to their new professor's slots
                for i in range(len(potential_professor.currentpositions)):
                    if potential_professor.currentpositions[i] is None:
                        potential_professor.currentpositions[i] = (potential_student, potential_prof_score)
                        #subtract 1 from the potential professor's open positions
                        potential_professor.positions_open -= 1
                        #if all positions are now filled, make field open False
                        if potential_professor.positions_open == 0:
                            potential_professor.open = False
                        #else add them back onto the list
                        else:
                            professors_to_be_matched.append(potential_professor)
                        break
                #assign new professor to student
                potential_student.pairedwith = (potential_professor, potential_prof_score)

            #else potential student's score is with their current professor is higher than potential professor, so put professor back into list
            else:
                if nextStudent[potential_professor.name] < len(students):
                    professors_to_be_matched.append(potential_professor)

    time.sleep(1)

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
    convert_to_parquet(students, professors)
    match(students, professors)
    results = fetch_sorted_results("matches.parquet")
    pretty_print_results(results)



           

            


            
        







        

    
  




