# niklibpy

This is a Python library that provides a set of utility functions for common programming tasks. The
library includes the following functions:

- `pmap`: A simple parallel map construction, using a thread pool executor. It takes an array of
   functions and executes them in parallel, returning the results in the same order as the input
   functions.

- `pipe`: Applies a series of functions to an input value, with the output of each function being
   passed as the input to the next function in the series. Returns the final output value after all
   functions have been applied.

- `apmap`: An asynchronous version of `pmap` that takes an array of async functions and executes
   them in parallel, returning the results in the same order as the input functions.

- `dig`: Attempts to retrieve a value from a nested data structure (dictionary or list) using a
   sequence of keys. If no key is found, it returns None.

- `bury`: Inserts a value into a nested data structure (dictionary or list) at a location specified
   by a sequence of keys. If the location does not exist, it creates the necessary structure to
   accommodate the value. If the data structure is a list and the key exceeds its current length, it
   extends the list with None values.
