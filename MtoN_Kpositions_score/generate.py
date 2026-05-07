import random
from models import Professor, Student

def generate_random_instance():
    num_students = random.randint(5, 20)
    num_professors = random.randint(3, 10)

    #NEW
    num_categories = random.randint(3, 6)

    k = 3

    print(f"There are {num_students} students to pair")
    print(f"There are {num_professors} professors with {k} open positions")
    print(f"There are currently {num_categories} of areas interest")

    students = [Student(name=f"S{i}", emplID=random.randint(1000, 9999)) for i in range(num_students)]
    professors = [Professor(name=f"P{i}", positions=k) for i in range(num_professors)]

    #assign scores
    for student in students:
        for i in range(num_categories):
            score = random.randint(0, 10)
            #add score to list
            student.interest_score_list.append(score)

    for professor in professors:
        for i in range(num_categories):
            score = random.randint(0, 10)
            professor.interest_score_list.append(score)


    return students, professors

# if __name__ == "__main__":
#     generate_random_instance()
