# decorator for timing functions
import psutil


def measure_performance(func):
    import time
    def wrapper(*args, **kwargs):
        initial_ram_usage = psutil.virtual_memory().used
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        final_ram_usage = psutil.virtual_memory().used

        print(f"Time elapsed: {end_time - start_time} seconds")
        print(f"RAM usage increase: {(final_ram_usage - initial_ram_usage) / (1024 * 1024)} MegaBytes")

        return result
    return wrapper
