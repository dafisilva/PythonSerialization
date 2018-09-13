import json, functools, time


# create time id
time_id = str(time.strftime("%d_%m_%Y_%H%M%S", time.gmtime()))


class test_class(object):
    def __init__(self, name, teacher, students):
        self.name = name
        self.teacher = teacher
        self.students = students

class test_subject(object):
    def __init__(self, id, name, email, phone):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone


# ------
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
            message = "Time of operation " + str(elapsed_time)

            #write measures to file = "filename"
            with open(filename, "w") as winfo:
                winfo.write(message)

        return f_to_run_func
    return a_decorator


def create_data():
    # read from init_info.txt

    read_info = open("init_info.txt", 'r')

    do_teacher = True
    do_name = True
    do_email = False
    do_phone = False

    teacher = None
    name = ""
    email = ""
    phones = {}
    students = []
    id = 0

    class_name = read_info.readline()

    for line in read_info.readlines():
        try:
            if do_name:
                name = line
                do_name = False
                do_email = True
                continue

            if do_email:
                email = line
                do_email = False
                do_phone = True

            if do_phone:
                if line == '--':
                    id += 1

                    if do_teacher:
                        teacher = test_subject(id, name, email, phones)
                        do_teacher = False
                    else:
                        subject = test_subject(id, name, email, phone)
                        students.append(subject)

                    phones = {}
                    subject = None
                    do_phone = False
                    do_name = True

                else:
                    phone_id, number = line.split()
                    phones[phone_id] = number


        except:
            continue

    read_info.close()

    # create class with info read from file
    my_class = test_class(class_name, teacher, students)

    return my_class


# serialise to json
@measures(time_id + "_serialize_to_json.txt")
def to_json(my_class):
    with open("data.json", "w") as wf:
        json.dump(my_class.__dict__, wf)


# deserialiaze from json
@measures(time_id + "_deserialize_from_json.txt")
def from_json():
    with open("data.json", "r") as rf:
        data = json.load(rf)


if __name__ == '__main__':
    my_class = create_data()

    to_json(my_class)

    from_json()
