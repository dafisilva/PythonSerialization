import json, functools, time


class test_class(object):
    def __init__(self, name, teacher, students):
        self.name = name
        self.teacher = teacher
        self.students = students

class test_subject(object):
    def __init__(self, id, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


# ------
def create_data():
    # read from init_info.txt
    import sys

    students = []
    id = 0

    class_name = sys.stdin.readline()

    name, email, phone = sys.stdin.readline().split()
    teacher = test_subject(name, email, phone)

    for line in sys.stdin.readlines():
        try:
            name, email, phone = line.split()

            id += 1
            student = test_subject(id, name, email, phone)
            students.append(student)

        except:
            continue

    # create class with info read from file
    my_class = test_class(class_name, teacher, students)

    return my_class


# serialise to json
def to_json(my_class):
    with open("data.json", "w") as wf:
        json.dump(my_class, wf)


# deserialiaze from json
def from_json():
    with open("data.json", "r") as rf:
        data = json.load(rf)


# decorator for statistics
def measures(filename):

    def a_decorator(func):
        @functools.wraps(func)

        def f_to_run_func(*args, **kwargs):
            #start measures
            begin_time = time.time()
            func(*args, **kwargs)
            #end measures
            end_time = time.time()

            elapsed_time = end_time - begin_time
            message = "Time of operation " + elapsed_time

            #write measures to file = "filename"
            with open(filename, "w") as winfo:
                winfo.write(message)

    return f_to_run_func


if __name__ == '__main__':
    my_class = create_data()

    @measures("serialize_to_json.txt")
    to_json(my_class)

    @measures("deserialize_from_json.txt")
    from_json()
