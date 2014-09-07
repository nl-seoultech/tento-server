from functools import singledispatch

from flask import jsonify as flask_jsonify

from ..music import Position


@singledispatch
def jsonable(arg):
    return arg


@jsonable.register(list)
def _(arg):
    return [jsonable(x) for x in arg]


@jsonable.register(tuple)
def _(arg):
    return (jsonable(x) for x in arg)


def jsonify(*args, **kwargs):
    kwargs = dict([(k, jsonable(v)) for k, v in kwargs.items()])
    for x in jsonable(args):
        for k, v in x.items():
            if k in kwargs:
                raise Exception("key duplicated. key: {}".format(k))
            kwargs[k] = v
    return flask_jsonify(**kwargs)
