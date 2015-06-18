__author__ = 'se416237'

from multiprocessing import Process


def run_many(count):
    import find_slot
    import utils
    import uuid
    result = 0
    for i in range(count):
        p, s = find_slot.run(str(uuid.uuid1()), utils.rand_location())
        if p is not None:
            result += 1
    print(result)


if __name__ == "__main__":
    import sys
    proc = int(sys.argv[1])
    count = int(sys.argv[2])
    p_list = {}
    for p in range(proc):
        p_list[p] = Process(target=run_many, args=(count,))
        #p_list[p].daemon = True
    for p in range(proc):
        p_list[p].start()
    for p in range(proc):
        p_list[p].join()
