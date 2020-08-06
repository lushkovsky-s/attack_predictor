from timeit import default_timer as timer

import storage


def count_stats(f):
    def wrapper(*args, **kw):
        start = timer()
        res = f(*args, **kw)
        end = timer()

        elapsed = end - start
        count, avg_time = storage.stats.get()

        new_count = count + 1
        new_avg_time = avg_time * count / new_count + elapsed / new_count
        
        storage.stats.set(new_count, new_avg_time)

        return res
    return wrapper
