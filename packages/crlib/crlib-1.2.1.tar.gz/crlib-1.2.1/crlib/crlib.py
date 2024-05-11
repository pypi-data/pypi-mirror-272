"""
CrLib is a pile of steamy lukewarm garbage that gives you
random functions.
"""

from .metadata import * # get dem numbers

# imports?
import lazy_import as l_import
import importlib
import inspect

def lazy_import(imports, level="leaf"):
    """Lazy import off a list. Semi-colon allows importing as, and slash allows try excepts. At sign is for from importing (e.g ["numpy;np", "ujson;json/json", "random@randint;r_int"])"""

    frame = inspect.currentframe().f_back

    if isinstance(imports, str):
        imports = [imports]

    for mod in imports:
        for i, attempt in enumerate(pmod := mod.split("/")):
            smod = attempt.split(";")

            if importlib.util.find_spec(
                (
                    atsplit := smod[0].split("@")
                )[0]
            ):
                if len(atsplit) > 1:
                    if len(smod) > 1:
                        mname = smod[~0]

                    else:
                        mname = atsplit[~0]

                    frame.f_globals[mname] = l_import.lazy_callable(smod[0].replace("@", "."))

                else:
                    frame.f_globals[smod[~0]] = l_import.lazy_module(smod[0], level=level)

                break

            elif i >= (len(pmod) - 1):
                raise ImportError(f"Could not import any of {pmod}")

            else:
                continue

lazy_import([
    "hashlib",
    "pprint",
    "traceback",
    "os",
    "lzma",
    "base64",
    "sys",
    "functools",
    "dill;pickle/pickle",
    "collections",
])

class subscriber:
    """Subscriber object for pubsub"""
    def __init__(self, topic, callback):
        self.topic = topic
        self.callback = callback
        self.sid = topic + chr(0) + hashlib.md5(pickle.dumps(callback)).hexdigest()

class pubsub:
    """Publish/Subscribe model"""
    def __init__(self):
        # cache of listeners
        self.cache = {}

    def publish(self, topic, args=[], kwargs={}, cache=None):
        """Publish to a channel, run all callbacks listed with args and kwargs as list/dict. Returns a list of return values, newest subbed to oldest."""
        # Slashes are tiered, e.g subscribing to foo/bar/baz will callback when foo or foo/bar or foo/bar/baz are published.

        try:
            # retrieve listeners
            subs = self.cache[topic]

        except KeyError:
            return

        returns = []
        for subber in subs:
            # callback listeners
            returns.append(subber.callback(*args, **kwargs))

        return returns

    def subscribe(self, topic, callback):
        """Subscribe to a topic"""

        try:
            # retrieve listeners
            subs = self.cache[topic]

        except KeyError:
            self.cache[topic] = []
            subs = self.cache[topic]

        subber = subscriber(topic, callback)
        subs.insert(0, subber)
        return subber.sid

    def unsubscribe(self, sid):
        """Unsubscribe to topic with SID generated from crlib.pubsub().subscribe()"""
        # split into topic/callback hash
        sidl = sid.split(chr(0))

        try:
            # retrieve listeners
            subs = self.cache[sidl[0]]

        except KeyError:
            raise KeyError("Topic of unsubscribed callback not found")

        # unsubscribe stuff
        for i, subber in enumerate(subs):
            if subber.sid == sid:
                del self.cache[sidl[0]][i]
                break

    def clear(self):
        """say bye bye to your cache"""
        self.cache = {} # bye bye

    def view(self):
        """PPrints the cache tree"""
        pprint.pprint(self.cache, indent=4)

def cfor(start, test, update):
    """C-style for loops using lambdas"""
    while test(start):
        yield start
        start = update(start)

def find_args(func):
    """Attempt to list all arguments of a callable function"""
    try:
        return list(
            map(
                str,
                str(
                    inspect.signature(
                        func
                    )
                )[1:-1].split(
                    ", "
                )
            )
        )

    except ValueError:
        # couldn't find signature
        return None

class recursion:
    """
    A recursion context manager.
    Be careful when using this, settings a recursionlimit
    too high can literally crash python. To use, do
    with crlib.recursion(69420):
        print("lalala")

    Warning, you can cause Python to segfault if recursion limit
    is set too high.
    """
    def __enter__(self):
        self.old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)

class defer(object):
    """Defers functions to the end of a function/context manager."""
    def __init__(self, f=None):
        self.tb = traceback

        if f == None:
            self.exits, self.args, self.kwargs = [], [], []

        elif callable(f):
            self.function = f

        else:
            raise TypeError("Defer requires a function")

    def __call__(self, *args, **kwargs):

        import sys

        exits, aargs, akwargs = [], [], []

        def ddefer(f, *args, **kwargs):
            if callable(f):
                exits.append(f)
                aargs.append(args)
                akwargs.append(kwargs)

            else:
                raise TypeError(f"Object {f} cannot be deferred.")

        err = False
        try:
            out = self.function(defer=ddefer, *args, **kwargs)

        except:
           sys.stderr.write(self.tb.format_exc())
           err = True

        for i in range(len(exits) - 1, -1, -1):
            exits[i](*aargs[i], **(akwargs[i]))

        if err:
            sys.exit()

    def __enter__(self):
        return self.fdefer

    def fdefer(self, f, *args, **kwargs):
        if callable(f):
            self.exits.append(f)
            self.args.append(args)
            self.kwargs.append(kwargs)

        else:
            raise TypeError(f"Object {f} cannot be deferred.")

    def __exit__(self, type, value, traceback):
        trace = self.tb.format_exc()
        err = False

        if not trace.startswith("None"):
            sys.stderr.write(self.tb.format_exc())
            err = True

        for i in range(len(exits) - 1, -1, -1):
            try:
                args, kwargs, curf = self.args[i], self.kwargs[i], self.exits[i]

                curf(*args, **kwargs)

            except:
                sys.stderr.write(self.tb.format_exc())
                err = True

        if err:
            sys.exit()

class suppress:
    """Suppress messages being printed from stdout or stdeerr in this context manager."""
    def __init__(self):
        self.old_stderr = sys.stderr

    def __enter__(self, err=False):
        self.old_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

        if not err:
            self.old_stderr = sys.stderr
            sys.stderr = open(os.devnull, "w")

    def __exit__(self, type, value, tb):
        sys.stdout.close()
        sys.stdout = self.old_stdout

        sys.stderr.close()
        sys.stderr = self.old_stderr

def blob(inf, outf="blob.py"):
    """Blobify files into a python file for easy pyinstallering and stuff"""
    with open(inf, "rb") as f:
        with open(outf, "w") as g:
            g.write(
                "import lzma,base64;data=lzma.decompress(base64.a85decode(\""
                + base64.a85encode(
                    lzma.compress(
                        f.read()
                    )
                ).decode(
                    "utf"
                ).replace(
                    "\\",
                    "{"
                ).replace(
                    "\"",
                    "}"
                )
                + "\".replace(\"{\", \"\\\\\").replace(\"}\", \"\\\"\").encode(\"utf\")))\n"
                + """def unblob(outf):
\tglobal data
\twith open(outf, "wb") as f:
\t\tf.write(data)"""
            )

def gc():
    """Nukes every variable in scope excluding ones beginning with underscores."""

    frame = inspect.currentframe().f_back

    garbage = []
    for var in frame.f_globals:
        if (not var.startswith("_")) and (not var in ["crlib", "gc"]):
            garbage.append(var)

    for var in garbage:
        del frame.f_globals[var]

    __import__("gc").collect()

def nh_cache(maxsize=128, usedeque=True, copy=False):
    """Self made implementation of functools.cache() that allows non-hashable objects with some performance losses. Typing is always unique. FIFO."""
    def generator(f):
        if usedeque:
            argcache, resultcache = collections.deque([]), collections.deque([])

        else:
            argcache, resultcache = [], []

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                cached_result = resultcache[argcache.index((args, kwargs))]

                if copy:
                    return deepcopy(cached_result)

                return cached_result

            except ValueError:
                result = f(*args, **kwargs)
                argcache.append((args, kwargs))
                resultcache.append(result)

                if len(resultcache) > maxsize:
                    if usedeque:
                        argcache.popleft()
                        resultcache.popleft()

                    else:
                        argcache.pop(0)
                        resultcache.pop(0)

                return result

        return wrapper

    return generator

def lru_cache(maxsize=128, typed=False, copy=False):
    # functools.lru_cache, but can deepcopy
    if not copy:
        return functools.lru_cache(maxsize, typed)

    else:
        def generator(f):
            cached_func = functools.lru_cache(maxsize, typed)(f)

            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                return deepcopy(cached_func(*args, **kwargs))

            return wrapper

        return generator

def deepcopy(obj):
    # More performant than copy.deepcopy
    return pickle.loads(pickle.dumps(obj))

def _get_full_exc_name(obj):
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__
    return module + '.' + obj.__class__.__name__

def silence(func):
    # Don't kill program on error
    try:
        return func()

    except Exception as exception:
        print(traceback.format_exc())
        return f"{_get_full_exc_name(exception)}: {str(exception)}"

def arrfind(arr, key, v):
    try:
        return next(i for i in arr if (key(i) == v))

    except StopIteration:
        return None
