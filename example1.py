import concurrent.futures as ccf
import time
import random

__LEVEL_LIM__ = 170  # THE LIMIT OF INNER LISTS LEVELING ( ~450 is an approximate cap due to recursion limits )
__INNER_ARR_CHANCE__ = 0.002  # THE PROBABILITY OF THE INNER LIST TO APPEAR
__INNERS_LIM__ = 670  # THE LIMIT OF TOTAL AMOUNT OF INNER LISTS

TOTAL_INTS = 0  # COUNTER OF THE AMOUNT OF INTEGERS
TOTAL_INNERS = 0  # COUNTER OF THE AMOUNT OF INNER LISTS CREATED

def generate_the_example_data(level: int = 0, items_count: int = 20):
    arr = []  # init the resulting array
    global TOTAL_INNERS  # connect global counter
    for i in range(items_count):  # iterate by amount of items_count
        # logging to spectate the data generation process
        # N | > M%, where:
        # - N - index of the inner array
        # - M% - data generation progress for the current array
        # > - arrowhead shows the level of the array that is currently filled
        print(f'{TOTAL_INNERS} | {"> " * (level + 1)}{round(i/items_count*10000)/100}%')  # logging purposes
        if TOTAL_INNERS < __INNERS_LIM__ \
                and level < __LEVEL_LIM__ \
                and random.random() < __INNER_ARR_CHANCE__:  # randomizing the inner list appearance
            TOTAL_INNERS += 1  # counter ++
            arr.append(generate_the_example_data(level + 1, items_count))  # recursive self-calling
        else:  # if not the random then append simple integer to the resulting list
            arr.append(random.randint(0, 100))
            global TOTAL_INTS  # connect global counter
            TOTAL_INTS += 1  # counter ++
    return arr  # return the actual created list


# function to flat the multilayered list into 1D-list
def flatten_completely(arr: list[list]):
    return [
        item  # the item
        for plist in arr  # for potential list in given array
        for item in (  # for item itself or the items in sublist if item is the list
            flatten_completely(plist) if isinstance(plist, list) else [plist]
        )
    ]


# function to flat the multilayered list into generator to crate 1D-list
def flatten_completely_iter(arr: list[list]):
    for item in arr:
        if isinstance(item, list):
            for iitem in flatten_completely_iter(item):
                yield iitem
        else:
            yield item


# variable to store new generated data
the_data = generate_the_example_data(items_count=2000)


# VARIANT 1 - STRAIGHTFORWARD
def v1(data: list[list]):
    flat = flatten_completely(data)  # flatten the data
    cum_avg = 0  # init the average value storage
    for item in flat:  # iterate through the flattened list
        cum_avg += item / TOTAL_INTS  # add a part of the total average
    return cum_avg  # return the average


# VARIANT 2 - GENERATOR


def v2(data: list[list]):
    cum_avg = 0  # init the average value storage
    # iterate through the flattened list as generator
    for item in flatten_completely_iter(data):
        cum_avg += item / TOTAL_INTS  # add a part of the total average
    return cum_avg  # return the average


# VARIANT 3 - MULTITHREADING


def v3(data: list):
    cum_avg = 0  # init the average value storage
    futures = []  # init the futures storage (storage for tasks)
    for item in data:  # iterate through initial data
        if isinstance(item, list):  # ... and if the item is list ...
            with ccf.ThreadPoolExecutor() as ex:  # ... we enter the ThreadPoolExecutor ...
                # ... and create the corresponding task ...
                # ... achieving the multi-threaded recursion ...
                futures.append(ex.submit(v3, item))
        else:  # ... but if the simple item ...
            cum_avg += item / TOTAL_INTS  # ... we count it to the total average

    # then we wait for the all futures ending their job
    for task in ccf.as_completed(futures):  # ... and for each completed ...
        cum_avg += task.result()  # ... we adjust the average data
    return cum_avg  # after all, return the average


# pprint(the_data, compact=True)

class TimeMeasurer:
    t = None

    def measure(self, silent=False):
        if self.t is None:
            self.t = time.time()
            if not silent:
                print("Measurements started!")
        else:
            if not silent:
                print(f"Measure: {time.time() - self.t} seconds!")
            self.t = time.time()


measurer = TimeMeasurer()
measurer.measure()
print(v1(the_data))
measurer.measure()
print(v2(the_data))
measurer.measure()
print(v3(the_data))
measurer.measure()
