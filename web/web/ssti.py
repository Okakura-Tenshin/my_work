import re

def find_class_positions(class_list, target_classes):
    # Regular expression to extract class names
    class_pattern = re.compile(r"<class '([^']+)'>")
    
    # Dictionary to store positions of target classes
    class_positions = {cls: [] for cls in target_classes}
    
    # Iterate through the list and find positions
    for index, class_entry in enumerate(class_list):
        match = class_pattern.match(class_entry)
        if match:
            class_name = match.group(1)
            if class_name in target_classes:
                class_positions[class_name].append(index)
    
    return class_positions

# Example usage
class_list = [
    "<class 'type'>", "<class 'weakref'>", "<class 'weakcallableproxy'>", "<class 'weakproxy'>",
    "<class 'int'>", "<class 'bytearray'>", "<class 'bytes'>", "<class 'list'>",
    "<class 'NoneType'>", "<class 'NotImplementedType'>", "<class 'traceback'>", "<class 'super'>",
    "<class 'range'>", "<class 'dict'>", "<class 'dict_keys'>", "<class 'dict_values'>",
    "<class 'dict_items'>", "<class 'odict_iterator'>", "<class 'set'>", "<class 'str'>",
    "<class 'slice'>", "<class 'staticmethod'>", "<class 'complex'>", "<class 'float'>",
    "<class 'frozenset'>", "<class 'property'>", "<class 'managedbuffer'>", "<class 'memoryview'>",
    "<class 'tuple'>", "<class 'enumerate'>", "<class 'reversed'>", "<class 'stderrprinter'>",
    "<class 'code'>", "<class 'frame'>", "<class 'builtin_function_or_method'>", "<class 'method'>",
    "<class 'function'>", "<class 'mappingproxy'>", "<class 'generator'>", "<class 'getset_descriptor'>",
    "<class 'wrapper_descriptor'>", "<class 'method-wrapper'>", "<class 'ellipsis'>", "<class 'member_descriptor'>",
    "<class 'types.SimpleNamespace'>", "<class 'PyCapsule'>", "<class 'longrange_iterator'>", "<class 'cell'>",
    "<class 'instancemethod'>", "<class 'classmethod_descriptor'>", "<class 'method_descriptor'>", "<class 'callable_iterator'>",
    "<class 'iterator'>", "<class 'coroutine'>", "<class 'coroutine_wrapper'>", "<class 'moduledef'>",
    "<class 'module'>", "<class 'EncodingMap'>", "<class 'fieldnameiterator'>", "<class 'formatteriterator'>",
    "<class 'filter'>", "<class 'map'>", "<class 'zip'>", "<class 'BaseException'>",
    "<class 'hamt'>", "<class 'hamt_array_node'>", "<class 'hamt_bitmap_node'>", "<class 'hamt_collision_node'>",
    "<class 'keys'>", "<class 'values'>", "<class 'items'>", "<class 'Context'>",
    "<class 'ContextVar'>", "<class 'Token'>", "<class 'Token.MISSING'>", "<class '_frozen_importlib._ModuleLock'>",
    "<class '_frozen_importlib._DummyModuleLock'>", "<class '_frozen_importlib._ModuleLockManager'>", "<class '_frozen_importlib._installed_safely'>", "<class '_frozen_importlib.ModuleSpec'>",
    "<class '_frozen_importlib.BuiltinImporter'>", "<class 'classmethod'>", "<class '_frozen_importlib.FrozenImporter'>", "<class '_frozen_importlib._ImportLockContext'>",
    "<class '_thread._localdummy'>", "<class '_thread._local'>", "<class '_thread.lock'>", "<class '_thread.RLock'>",
    "<class 'zipimport.zipimporter'>", "<class '_frozen_importlib_external.WindowsRegistryFinder'>", "<class '_frozen_importlib_external._LoaderBasics'>", "<class '_frozen_importlib_external.FileLoader'>",
    "<class '_frozen_importlib_external._NamespacePath'>", "<class '_frozen_importlib_external._NamespaceLoader'>", "<class '_frozen_importlib_external.PathFinder'>", "<class '_frozen_importlib_external.FileFinder'>",
    "<class '_io._IOBase'>", "<class '_io._BytesIOBuffer'>", "<class '_io.IncrementalNewlineDecoder'>", "<class 'posix.ScandirIterator'>",
    "<class 'posix.DirEntry'>", "<class 'codecs.Codec'>", "<class 'codecs.IncrementalEncoder'>", "<class 'codecs.IncrementalDecoder'>",
    "<class 'codecs.StreamReaderWriter'>", "<class 'codecs.StreamRecoder'>", "<class '_abc_data'>", "<class 'abc.ABC'>",
    "<class 'dict_itemiterator'>", "<class 'collections.abc.Hashable'>", "<class 'collections.abc.Awaitable'>", "<class 'collections.abc.AsyncIterable'>",
    "<class 'async_generator'>", "<class 'collections.abc.Iterable'>", "<class 'bytes_iterator'>", "<class 'bytearray_iterator'>",
    "<class 'dict_keyiterator'>", "<class 'dict_valueiterator'>", "<class 'list_iterator'>", "<class 'list_reverseiterator'>",
    "<class 'range_iterator'>", "<class 'set_iterator'>", "<class 'str_iterator'>", "<class 'tuple_iterator'>",
    "<class 'collections.abc.Sized'>", "<class 'collections.abc.Container'>", "<class 'collections.abc.Callable'>", "<class 'os._wrap_close'>",
    "<class '_sitebuiltins.Quitter'>", "<class '_sitebuiltins._Printer'>", "<class '_sitebuiltins._Helper'>", "<class 'functools.partial'>",
    "<class 'functools._lru_cache_wrapper'>", "<class 'operator.attrgetter'>", "<class 'operator.itemgetter'>", "<class 'operator.itemgetter'>",
    "<class 'operator.attrgetter'>", "<class 'operator.methodcaller'>", "<class 'itertools.accumulate'>", "<class 'itertools.combinations'>",
    "<class 'itertools.combinations_with_replacement'>", "<class 'itertools.cycle'>", "<class 'itertools.dropwhile'>", "<class 'itertools.takewhile'>",
    "<class 'itertools.islice'>", "<class 'itertools.starmap'>", "<class 'itertools.chain'>", "<class 'itertools.compress'>",
    "<class 'itertools.filterfalse'>", "<class 'itertools.count'>", "<class 'itertools.zip_longest'>", "<class 'itertools.permutations'>",
    "<class 'itertools.product'>", "<class 'itertools.repeat'>", "<class 'itertools.groupby'>", "<class 'itertools._grouper'>",
    "<class 'itertools._tee'>", "<class 'itertools._tee_dataobject'>", "<class 'reprlib.Repr'>", "<class 'collections.deque'>",
    "<class '_collections._deque_iterator'>", "<class '_collections._deque_reverse_iterator'>", "<class 'collections._Link'>", "<class 'functools.partialmethod'>",
    "<class 'types.DynamicClassAttribute'>", "<class 'types._GeneratorWrapper'>", "<class 'enum.auto'>", "<enum 'Enum'>",
    "<class 're.Pattern'>", "<class 're.Match'>", "<class '_sre.SRE_Scanner'>", "<class 'sre_parse.Pattern'>",
    "<class 'sre_parse.SubPattern'>", "<class 'sre_parse.Tokenizer'>", "<class 're.Scanner'>", "<class 'string.Template'>",
    "<class 'string.Formatter'>", "<class 'contextlib.ContextDecorator'>", "<class 'contextlib._GeneratorContextManagerBase'>", "<class 'contextlib._BaseExitStack'>",
    "<class 'typing._Final'>", "<class 'typing._Immutable'>", "<class 'typing.Generic'>", "<class 'typing._TypingEmpty'>",
    "<class 'typing._TypingEllipsis'>", "<class 'typing.NamedTuple'>", "<class 'typing.io'>", "<class 'typing.re'>",
    "<class '_ast.AST'>", "<class 'markupsafe._MarkupEscapeHelper'>", "<class 'warnings.WarningMessage'>", "<class 'warnings.catch_warnings'>",
    "<class 'zlib.Compress'>", "<class 'zlib.Decompress'>", "<class 'tokenize.Untokenizer'>", "<class 'traceback.FrameSummary'>",
    "<class 'traceback.TracebackException'>", "<class '_weakrefset._IterationGuard'>", "<class '_weakrefset.WeakSet'>", "<class 'threading._RLock'>",
    "<class 'threading.Condition'>"
]

target_classes = ['open']

positions = find_class_positions(class_list, target_classes)
print(positions)
