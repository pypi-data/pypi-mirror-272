'''Mostly useless serialization format.

This is a format based on a series of keys and values, and optional list
values.

Effectively, the format is a list of ``key|value`` lines, where keys may be
made into a list by either repeating them or suffixing them with an _1 index,
incrementing.
'''
from collections.abc import Sequence
from io import StringIO
from typing import Union, Mapping, Sequence, TextIO, Optional, Tuple, Callable, MutableMapping, MutableSequence, List

ValueList = Sequence[str]
Value = Union[str, ValueList]
Object = Mapping[str, Value]

# Mutable list that can be appended to.
MutableList = MutableSequence[str]
MutableValue = Union[str, MutableList]

class WorkValue:
    '''A working parsing list for actively parsing values in.

    This is used for splitting plain and indexed values, and elegantly handling
    multiple plain values, or plain and indexed values appearing together with
    the same key.

    These conditions are technically illegal, but we don't enforce them.
    '''

    def __init__(
        self,
        plain: Optional[MutableSequence] = None,
        indexed: Optional[List[Tuple[int, str]]] = None) -> None:
        if plain is None:
            plain = []
        if indexed is None:
            indexed = []

        self.plain = plain
        self.indexed = indexed
        
    

    def _single(self) -> bool:
        return len(self.plain) == 1 and len(self.indexed) == 0

    def value(self, list_class: Callable[[], MutableList] = list) -> MutableValue:
        '''If there is just a single plain value, return that, otherwise return
        a list of all the plain values followed by all the indexed values sorted by
        index.

        '''
        if self._single():
            return self.plain[0]
        else:
            list = list_class()

            for item in self.plain:
                list.append(item)

            self.indexed.sort(key=lambda i: i[0])

            for _, item in self.indexed:
                list.append(item)

            return list

WorkObject = MutableMapping[str, WorkValue]
MutableObject = MutableMapping[str, MutableValue]

def dump(obj: Object, fp: TextIO, startindex: int = 1, separator: str = '|', index_separator: str = '_'):
    '''Dump an object in req format to the fp given.

    If there are redundant elements (like in ``{'Foo': ['Bar'], 'Foo_1': 'Bar'}}``)
    the first encountered equivalent key will always be the only one written.

    :param obj: The object to serialize.
    :param fp: A writable that can accept all the types given.
    :param separator: The separator between key and value.
    :param index_separator: The separator between key and index.
    '''

    if startindex < 0:
        raise ValueError('startindex must be non-negative, but was {}'.format(startindex))

    keys = set()

    for key, value in obj.items():
        if isinstance(value, str):
            if key not in keys:
                fp.write(key)
                fp.write(separator)
                fp.write(value)
                fp.write('\n')
                keys.add(key)
        else:
            for index, item in enumerate(value, start=startindex):
                k = index_separator.join((key, str(index)))
                if k not in keys:
                    fp.write(k)
                    fp.write(separator)
                    fp.write(item)
                    fp.write('\n')
                    keys.add(k)

def dumps(obj: Object, startindex: int = 1, separator: str = '|', index_separator: str = '_') -> str:
    '''Dump an object in req format to a string.

    :param obj: The object to serialize.
    :param separator: The separator between key and value.
    :param index_separator: The separator between key and index.
    '''

    io = StringIO()

    dump(
        obj=obj,
        fp=io,
        startindex=startindex,
        separator=separator,
        index_separator=index_separator,
        )

    return io.getvalue()

def load(
    fp: TextIO,
    keep_originals: bool = False,
    separator: str = '|',
    index_separator: str = '_',
    dict_class: Callable[[], MutableObject] = dict,
    list_class: Callable[[], MutableList] = list,
    work_dict_class: Callable[[], WorkObject] = dict) -> Object:

    '''Load an object from the file pointer.

    :param fp: A readable filehandle.
    :param keep_originals: If True, keep the original indexed lines as well.
    :param separator: The separator between key and value.
    :param index_separator: The separator between key and index.
    '''

    work = work_dict_class()

    for line in fp:
        line = line.strip()
        if line:
            key, value = line.split(separator, 1)

            keyparts = key.rsplit(index_separator, 1)

            try:
                index = int(keyparts[1])

                work_key = keyparts[0]
            except (ValueError, IndexError):
                index = None
                work_key = key

            if work_key in work:
                work_value = work[work_key]
            else:
                work_value = WorkValue()
                work[work_key] = work_value

            if index is None:
                work_value.plain.append(value)

            else:
                work_value.indexed.append((index, value))

                if keep_originals:
                    if key in work:
                        work_value = work[key]
                    else:
                        work_value = WorkValue()
                        work[key] = work_value
                    work_value.plain.append(value)

    output = dict_class()


    for key, work_value in work.items():
        output[key] = work_value.value(list_class=list_class)

    return output

def loads(
    s: str,
    keep_originals: bool = False,
    separator: str = '|',
    index_separator: str = '_',
    dict_class: Callable[[], MutableObject] = dict,
    list_class: Callable[[], MutableList] = list,
    work_dict_class: Callable[[], WorkObject] = dict) -> Object:
    '''Loads an object from a string.

    :param s: An object to parse
    :param keep_originals: If True, keep the original indexed lines as well.
    :param separator: The separator between key and value.
    :param index_separator: The separator between key and index.
    '''

    io = StringIO(s)

    return load(
        fp=io,
        keep_originals=keep_originals,
        separator=separator,
        index_separator=index_separator,
        dict_class=dict_class,
        list_class=list_class,
        work_dict_class=work_dict_class,
        )
