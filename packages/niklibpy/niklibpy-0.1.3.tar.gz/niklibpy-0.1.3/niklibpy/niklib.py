import asyncio
import concurrent.futures
import copy
import warnings
from functools import reduce, partial
from typing import Any, Callable, List, Union


def pmap(funcs: List[Callable], max_workers: int = 2) -> List[Any]:
    """Simple parallel map construction, using a thread pool executor.

    Feed it an array of functions, and it will execute them in parallel, returning
    the results in the same order as the input functions"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(func): i for i, func in enumerate(funcs)}
        results = []
        for future, i in futures.items():
            try:
                result = future.result()
            except Exception as e:
                warnings.warn(f"Function {i} raised an exception: {e}")
                result = None
            results.append((i, result))
        results.sort()
        return [result for i, result in results]


async def apmap(funcs: List[Callable]) -> List[Any]:
    """Asynchronous parallel map construction, using asyncio.

    Feed it an array of async functions, and it will execute them in parallel, returning the results
    in the same order as the input functions"""

    async def run_func(i, func):
        try:
            return i, await func()
        except Exception as e:
            warnings.warn(f"Function {i} raised an exception: {e}")
            return i, None

    tasks = [asyncio.create_task(run_func(i, func)) for i, func in enumerate(funcs)]
    results = await asyncio.gather(*tasks)
    results.sort()
    return [result for i, result in results]


def pipe(
    inp: Any,
    *fns: Callable[..., Any],
    debug: bool = False,
    debug_print_fn: Callable = print,
) -> Any:
    """
    Applies a series of functions to an input value, with the output of each function
    being passed as the input to the next function in the series. Returns the final
    output value after all functions have been applied. If debug is True, uses
    debug_print_fn to print the input and output of each function.

    :param inp: The initial input value
    :param fns: A variable-length list of functions to apply to the input value
    :param debug: If True, prints the input and output of each function using debug_print_fn
    :param debug_print_fn: The function used for printing debug information (default is print)
    :return: The final output value after all functions have been applied
    """

    def debug_wrapper(fn, input_value):
        output_value = fn(input_value)
        try:
            debug_print_fn(
                f"<pipe> Function: {fn.__name__}, Input: '{input_value}', Output: '{output_value}'"
            )
        except:
            pass
        return output_value

    for fn in fns:
        if inp is None:
            return None
        if debug:
            inp = debug_wrapper(fn, inp)
        else:
            inp = fn(inp)
    return inp


def dig(data: Union[dict, list], *keys: Any) -> Any:
    """
    Attempts to retrieve a value from a nested data structure (dictionary or list)
    using a sequence of keys. If no key is found, it returns None.

    :param data: The initial data structure (dictionary or list)
    :param keys: A variable-length list of keys to traverse the data structure
    :return: The value found at the end of the key sequence, or None if any key is not found
    """
    for key in keys:
        if isinstance(data, (dict, list)):
            try:
                data = data[key]
            except (KeyError, IndexError, TypeError):
                return None
        else:
            return None
    return data


def bury(
    data: Union[dict, list], keys: List[Any], value: Any, in_place: bool = True
) -> Union[dict, list]:
    """
    Inserts a value into a nested data structure (dictionary or list) at a
    location specified by a sequence of keys. If the location does not exist,
    it creates the necessary structure to accommodate the value. If the data
    structure is a list and the key exceeds its current length, it extends the
    list with None values.

    :param data: The initial data structure (dictionary or list)
    :param keys: A list of keys specifying the location to insert the value
    :param value: The value to be inserted
    :param in_place: If True, modifies the original data structure. If False,
     creates a deep copy of the data structure and modifies that.
    :return: The modified data structure
    """
    if not in_place:
        data = copy.deepcopy(data)

    current = data
    for i, key in enumerate(keys):
        if i == len(keys) - 1:
            if isinstance(current, list) and key >= len(current):
                current.extend([None] * (key - len(current) + 1))
            current[key] = value
        else:
            if isinstance(current, dict):
                current = current.setdefault(key, {})
            elif isinstance(current, list):
                while len(current) <= key:
                    current.append({})
                current = current[key]
            else:
                raise TypeError(
                    "Cannot bury value in non-dictionary or non-list object"
                )

    return data
