from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable, TypeVar, Union

T = TypeVar('T')
R = TypeVar('R')

def parallel_do(items: List[T], func: Callable[[T], R]) -> List[Union[R, None]]:
    """
    Process an array of items in parallel while maintaining the order of results.

    :param items: List of items to be processed.
    :param func: A function that takes an item and returns a result.
    :return: A list of results corresponding to the input items.
    """
    results: List[Union[R, None]] = [None] * len(items)  # Pre-allocate the result list to maintain order

    with ThreadPoolExecutor() as executor:
        # Map each item to a future
        future_to_index = {executor.submit(func, item): i for i, item in enumerate(items)}

        # As tasks complete, store results in the appropriate position
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            results[index] = future.result()

    return results