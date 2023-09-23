"""list_helper offers tools to work with lists, mostly using the ``itertools`` library."""

import itertools


def flatten(nested_list):
    return list(itertools.chain.from_iterable(nested_list))


def remove_duplicate_dicts(list_of_dicts):
    results = []
    for element in list_of_dicts:
        if element not in results:
            results.append(element)
    return results
