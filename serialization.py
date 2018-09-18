import msgpack, json, functools, time, statistics, sys, os


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
            message = ""
            n_loops = 30
            time_sample = []
            size_sample = []

            for i in range(n_loops):
                #start measures
                begin_time = time.time()
                objfile = func(*args, **kwargs)
                #end measures
                end_time = time.time()

                # iteration statistics
                elapsed_time = end_time - begin_time
                time_sample.append(elapsed_time)

                if isinstance(objfile, dict):
                    # we are returned a dict from the json or msgpack so, we need to populate the test_class object before verifying it's size
                    my_class = test_class(None, None, None)
                    my_class.__dict__ = objfile
                    object_size = sys.getsizeof(my_class)
                else:
                    object_size = os.path.getsize(objfile)
                size_sample.append(object_size)

                loop_result = "Loop (" + str(i + 1) + ") - Time: " + str(elapsed_time) + " (s)\t\t - size of file/object created: " + str(object_size) + "(Bytes)\n"
                message += loop_result

            # final statistics
            time_stdev = statistics.stdev(time_sample)
            time_mean = statistics.mean(time_sample)
            size_stdev = statistics.stdev(size_sample)
            size_mean = statistics.mean(size_sample)

            message += "\nFinal statics:\n"
            message += "\tAverage time of operation: " + str(time_mean) + " (s)\n"
            message += "\tStandard deviation concerning operation time: " + str(time_stdev) + " (s)\n"
            message += "\tAverage size of file created: " + str(size_mean) + " (bytes)\n"
            message += "\tStandard deviation of the size of the file created: " + str(size_stdev) + " (bytes)\n"

            # write measures to file = "filename"
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

        if do_name:
            name = line
            do_name = False
            do_email = True
            continue

        if do_email:
            email = line
            do_email = False
            do_phone = True
            continue

        if do_phone:
            if line == '--\n':
                id += 1

                if do_teacher:
                    teacher = test_subject(id, name, email, phones)
                    do_teacher = False
                else:
                    subject = test_subject(id, name, email, phones)
                    students.append(subject)
                    subject = None

                phones = {}
                do_phone = False
                do_name = True
                continue

            else:
                phone_id, number = line.split()
                phones[phone_id] = number
                continue

    read_info.close()

    # create class with info read from file
    my_class = test_class(class_name, teacher, students)

    message = "Elements in class: " + str(id)
    message += "\nSize of class: " + str(sys.getsizeof(my_class)) + " (Bytes)"

    with open(time_id + "_init_status.txt", "w") as wf:
        wf.write(message)

    return my_class


# serialise to json
@measures(time_id + "_serialize_to_json.txt")
def to_json(my_class):
    with open("data.json", "w") as wf:
        json.dump(my_class.__dict__, wf, default=lambda o: o.__dict__)

    return "data.json"


# deserialiase from json
@measures(time_id + "_deserialize_from_json.txt")
def from_json():
    data = None
    with open("data.json", "r") as rf:
        data = json.load(rf)

    return data


# serialise to msgpack
@measures(time_id + "_serialize_to_msgpack.txt")
def to_msgpack(my_class):
    with open("data.msgpack", "wb") as wf:
        msgpack.pack(my_class.__dict__, wf,  default=lambda o: o.__dict__)

    return "data.msgpack"


# deserialiase from msgpack
@measures(time_id + "_deserialize_from_msgpack.txt")
def from_msgpack():
    data = None
    with open("data.msgpack", "rb") as rf:
        data = msgpack.unpack(rf)

    return data



if __name__ == '__main__':
    my_class = create_data()

    to_json(my_class)

    from_json()

    to_msgpack(my_class)

    from_msgpack()
