# line no in csv, start with 2
def run_specified(func):
    def wrapper(*args, **kwargs):
        start = kwargs.pop('start', None)
        stop = kwargs.pop('stop', None)
        linenos = kwargs.pop('linenos', None)
        cases = func(*args, **kwargs)
        if isinstance(linenos, tuple):
            return [x for i, x in enumerate(cases) if i + 2 in linenos]
        else:
            if isinstance(start, int):
                start = start - 2 if start >= 2 else 2
            if isinstance(stop, int):
                stop = stop - 1 if stop < len(cases) + 1 else None
            return cases[start:stop]
    return wrapper
