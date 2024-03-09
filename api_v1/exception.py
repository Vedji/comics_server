class NotExists(Exception):
    pass


class AppendCollision(Exception):
    pass


def req_fun(key, name: str = "", default=None):
    try:
        data = key()
        return data, {"status": "success"}, None
    except AppendCollision as body:
        return default, {"status": "error", "message": body.__str__(), "code": 409}, AppendCollision
    except NotExists as body:
        return default, {"status": "error", "message": body.__str__(), "code": 404}, NotExists


def get_arg(value, key, name: str = "", default=None):
    try:
        value = key(value)
    except ValueError:
        return default, {"status": "error", "message": f"Argument {name} is not integer", "code": 422}, ValueError
    except KeyError:
        return default, {"status": "error", "message": f"Argument {name} is not exists", "code": 400}, KeyError
    except TypeError:
        return default, {"status": "error", "message": f"Argument {name} is uncorrected", "code": 400}, TypeError
    return value, {"status": "success"}, True
