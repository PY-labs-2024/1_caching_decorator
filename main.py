def caching_decorator(max_cache_depth=100):
    cache_dict = {}  # Словарь для хранения кэшей всех функций

    def real_decorator(function):
        def wrapper(*args, **kwargs):
            func_name = function.__name__
            # Смотрим, есть ли кэш для данной функции
            if func_name in cache_dict:
                # Есть ли кэш для таких аргументов
                if args in cache_dict[func_name]:
                    return cache_dict[func_name][args]

                # Раз для данных значений кэша нет -> считаем его
                result = function(*args, **kwargs)

                # Если складывать некуда, то удаляем самый старый
                if len(cache_dict[func_name]) >= max_cache_depth:
                    cache_dict[func_name].pop(next(iter(cache_dict[func_name])))

                # Добавляем новое значение в кэш
                cache_dict[func_name][args] = result
                return result

            # Раз для данной функции кэша ещё нет, то создаем его
            result = function(*args, **kwargs)
            cache_dict[func_name] = {args: result}
            return result

        return wrapper

    return real_decorator


if __name__ == '__main__':
    @caching_decorator(2)
    def double(x):
        print(f"Считаю значение функции double при параметре {x}")
        return x * 2


    @caching_decorator(3)
    def triple(x):
        print(f"Считаю значение функции triple при параметре {x}")
        return x * 3


    print('double(1): ', double(1))
    print('double(2): ', double(2))
    print('double(3): ', double(3))

    print()
    print('triple(1)', triple(1))
    print('triple(2)', triple(2))
    print('triple(3)', triple(3))

    print('triple(1)', triple(1))
    print('triple(2)', triple(2))
    print('triple(3)', triple(3))

    print()
    print('double(3): ', double(3))
    print('double(2): ', double(2))
    print('double(1): ', double(1))

    print("\nКак видно из вывода, для функции triple с глубиной кэша 3, значения посчитались единожды, "
          "а для функции double с глубиной кэша 2 одно из значений пришлось пересчитать")
