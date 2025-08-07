from enum import Enum


class Exam(Enum):
    Math = "Math"
    Physics = "Physics"
    Chemistry = "Chemistry"
    Computer_Science = "Computer_Science"
    Admission = "Admission"


class Applicant:

    def __init__(self, name, exam: dict, priority):
        self._fullname = name
        self._exam_score = exam
        self._priority = priority
        self._is_accepted = False

    @property
    def fullname(self):
        return self._fullname

    def get_exam(self, *keys):
        if len(keys) == 0:
            return None
        list_score = [self._exam_score[keys[i]] for i in range(len(keys))]
        avg_score = round(sum(list_score) / len(list_score), 1)
        return max(avg_score, self._exam_score[Exam.Admission])

    @property
    def is_accepted(self):
        return self._is_accepted

    @is_accepted.setter
    def is_accepted(self, value):
        self._is_accepted = self._is_accepted or value

    def get_priority(self, index):
        return self._priority[index]

    def __str__(self):
        return f"{self._fullname}"

    def __repr__(self):
        return f"{self._fullname} {self._exam_score} {self.is_accepted} {self._priority}"


class Department:

    def __init__(self, name, size):
        self.name = name
        self._size = size
        self._students = []

    def need_exam(self):
        match self.name:
            case "Mathematics":
                return [Exam.Math]
            case "Physics":
                return [Exam.Physics, Exam.Math]
            case "Biotech":
                return [Exam.Chemistry, Exam.Physics]
            case "Chemistry":
                return [Exam.Chemistry]
            case "Engineering":
                return [Exam.Computer_Science, Exam.Math]
            case _:
                return None

    def receive_application(self, applicant: Applicant):
        if len(self._students) < self._size and not applicant.is_accepted:
            self._students.append(applicant)
            return True
        else:
            return False

    def close_reception(self):
        try:
            with open(f'{self.name.lower()}.txt', 'w') as file:
                for student in (sorted(self._students,
                                       key=lambda applicant:
                                       (-applicant.get_exam(*self.need_exam()), applicant.fullname)
                                       )):
                    file.write(f"{student.fullname} {student.get_exam(*self.need_exam())}\n")
        except Exception:
            print(f"Could not write to file {self.name.lower()}.txt")
            pass

    def __str__(self):
        message = self.name + " " + f"{len(self._students)}"
        for student in (sorted(self._students,
                               key=lambda applicant:
                                    (-applicant.get_exam(*self.need_exam()), applicant.fullname)
                               )):
            message += f"\n{student} {student.get_exam(*self.need_exam())}"
        return message + "\n"


class Reception:

    def __init__(self):
        self._list_applicant = []
        self.from_files()

    def from_files(self):
        try:
            with open('applicants.txt', 'r') as file:
                for line in file.readlines():
                    first_name, last_name, physics, chemistry, math, computer_science, admission, dept_1, dept_2, dept_3 = line.split()
                    exam_score = {Exam.Physics: int(physics),
                                  Exam.Chemistry: int(chemistry),
                                  Exam.Math: int(math),
                                  Exam.Computer_Science: int(computer_science),
                                  Exam.Admission: int(admission)}
                    self._list_applicant.append(
                        Applicant(first_name + ' ' + last_name, exam_score, [dept_1, dept_2, dept_3])
                    )
        except FileNotFoundError:
            print("File not found")

    def get_not_accepted(self):
        return list(filter(lambda applicant: not applicant.is_accepted, self._list_applicant))


if __name__ == '__main__':

    reception = Reception()

    number_place = int(input())
    list_department = [Department("Mathematics", number_place),
                       Department("Physics", number_place),
                       Department("Biotech", number_place),
                       Department("Chemistry", number_place),
                       Department("Engineering", number_place)]
    list_department = list(sorted(list_department, key=lambda depart: depart.name))

    for turn in range(3):
        for department in list_department:
            ranking_list = [applicant for applicant in reception.get_not_accepted() if
                            department.name == applicant.get_priority(turn)]
            ranking_list = sorted(ranking_list, key=lambda applicant: (-applicant.get_exam(*department.need_exam()), applicant.fullname))

            for applicant in ranking_list:
                applicant.is_accepted = department.receive_application(applicant)

    for department in sorted(list_department, key=lambda depart: depart.name):
        department.close_reception()
