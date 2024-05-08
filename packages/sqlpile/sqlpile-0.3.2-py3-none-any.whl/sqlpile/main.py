import functools
import inspect
import time

from loguru import logger
from rich import print
from supamodel import supabase_client
from toolz import curry

from sqlpile.abcs import BaseCache
from sqlpile.config import settings as config
from sqlpile.core import MultiLayerCache, SQLCache, SupabaseCache
from sqlpile.utils import hash_code, recursive_hash


def get_layered_cache():
    remote = SupabaseCache(supabase_client)
    local = SQLCache(config.local_db_uri)
    cache = MultiLayerCache(local, remote)
    return cache


# Create curry function of dogpile
cache = get_layered_cache()
multi_layer_cache: MultiLayerCache = cache
sqlcache = multi_layer_cache


def dogpile(cache_instance: BaseCache):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            raw_key = (func.__name__, args, tuple(sorted(kwargs.items())))
            result = cache_instance.get(raw_key)
            if result is not None:
                return result
            else:
                result = func(*args, **kwargs)
                cache_instance.set(raw_key, result)
                return result

        return wrapper

    return decorator


def supacache_cache(ignore_params=[], verbose=False):
    """Decorator to cache function output based on its inputs, using Redis.
    Ignores specified parameters for caching purposes."""

    def decorator(func):
        if not multi_layer_cache:
            return func  # Skip caching if in debug mode

        func_source_code_hash = hash_code(inspect.getsource(func))

        def wrapper(*args, **kwargs):
            # Prepare args and kwargs for hashing
            args_names = func.__code__.co_varnames[: func.__code__.co_argcount]
            args_dict = dict(zip(args_names, args))

            # Remove ignored params from args and kwargs
            for param in ignore_params:
                args_dict.pop(param, None)
                kwargs.pop(param, None)

            # Create a unique cache key
            cache_key = (
                func.__module__
                + ":"
                + func.__name__
                + ":"
                + recursive_hash((args_dict, kwargs), ignore_params=ignore_params)
                + ":"
                + func_source_code_hash
            )

            # Attempt to retrieve the cached result
            cached_result = multi_layer_cache.get(cache_key)
            if cached_result:
                if verbose:
                    print("Used cache for function: " + func.__name__)
                return cached_result

            # Execute the function and cache the result if no cache is found
            result = func(*args, **kwargs)
            try:
                # Cache the result using the unique cache key
                multi_layer_cache.set(cache_key, result)
            except Exception as e:
                if verbose:
                    print(f"Caching failed for function: {func.__name__}, Error: {e}")

            return result

        return wrapper

    return decorator


# def get_layered_cache():
#     remote = SupabaseCache(supabase_client)
#     local = SQLCache(config.local_db_uri)
#     cache = MultiLayerCache(local, remote)
#     return cache


# Create curry function of dogpile
cache = get_layered_cache()
dogpile = curry(dogpile)
sqlpile = dogpile(cache_instance=cache)
# sqlpile = curry(dogpile)(cache_instance=layered_cache)


@sqlpile
def example_function():
    time.sleep(10)
    return 42


def main():
    #  Try out cache functions
    # Use magic methods too
    # print()
    cache.set("key", 42)
    print(cache["key"])
    print("key" in cache)
    for i in range(10):
        logger.debug("Starting example function")
        example_function()
        logger.success("Finished example function")
    # del cache["key"]


if __name__ == "__main__":
    main()
