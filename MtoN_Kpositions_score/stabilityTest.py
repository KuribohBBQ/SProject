import duckdb as db
import random
from collections import deque
from models import Professor, Student
from dataclasses import dataclass, field
from typing import List, Optional
import time
import duckdb as db
from generate import generate_random_instance
from matchM_to_N_score import match
from calc_compatibility import calculate_compatibility



def stability_check_score(listof_students, listof_professors, parquet_file="matches.parquet"):
    unstablecnt = 0
    

    for student in listof_students:
        current_prof = None
        current_score = -1

        if student.pairedwith is not None:
            current_prof, current_score = student.pairedwith

        for professor in listof_professors:
            # skip the professor the student already has
            if current_prof is not None and professor.name == current_prof.name:
                continue

            pair_score = calculate_compatibility(
            studentscores=student.interest_score_list,
            professorscores=professor.interest_score_list
)

            #Student does not prefer this professor over current match
            if pair_score <= current_score:
                continue

            # Case 1: professor has an open slot
            if professor.positions_open > 0:
                print(
                    f"Unstable: {student.name} and {professor.name} "
                    f"prefer each other. Score: {pair_score:.3f}"
                )
                unstablecnt += 1
                continue

            # Case 2: professor is full, but prefers this student
            worst_current_score = min(
                entry[1]
                for entry in professor.currentpositions
                if entry is not None
            )

            if pair_score > worst_current_score:
                print(
                    f"Unstable: {student.name} and {professor.name}. "
                    f"{professor.name}'s worst current score is {worst_current_score:.3f}, "
                    f"but {student.name}'s score is {pair_score:.3f}"
                )
                unstablecnt += 1

    print(f"Total unstable matchings found: {unstablecnt}\n")

if __name__ == "__main__":
    print("Begin stability testing")
    students, professors = generate_random_instance()
    match(students, professors)
    stability_check_score(students, professors)