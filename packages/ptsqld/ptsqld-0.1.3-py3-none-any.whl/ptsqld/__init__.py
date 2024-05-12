from os.path import exists
from datetime import datetime
from sqlton import parse
from sqlton.ast import Select, Values, All
from sqletic import Engine as _Engine
from functools import partialmethod
from echovault import Vault as _Vault 
from echovault.list import List as _List 
from echovault.dict import Dict as _Dict 
from dulwich.object_store import DiskObjectStore, MemoryObjectStore
from dulwich.refs import DiskRefsContainer, DictRefsContainer
from random import choices, randint
from string import ascii_letters, digits
from weakref import WeakSet

class Vault(_Vault):
    class List(_List):
        class Dict(_Dict):
            def __setitem__(self, key, value):
                table_name = self.container.identifier

                if table_name == b'__schema':
                    super().__setitem__(key, value)
                    return
                
                (_, schema), = (table
                                for table in self.container.container['__schema']
                                if table['name'] == table_name)

                if key not in schema.keys():
                    raise KeyError(f"{key} not one of the keys part of table {table_name} schema")

                super().__setitem__(key, value)

        def extend(self, iterable):
            table_name = self.identifier.decode('utf-8')

            if table_name == '__schema':
                super().extend(iterable)
                return
            
            def filler(iterable):
                for table in self.container['__schema']:
                    if table['name'] == table_name:
                        break
                else:
                    raise KeyError(f'No table {table_name} in schema')

                schema = table['description']
                
                for entry in iterable:
                    _entry = {} | entry
                    
                    if unexpected_keys := (set(entry.keys()) - set(schema.keys())):
                        raise KeyValue(f'those {unexpected_keys} keys are not expected in table {table_name}')
                    
                    for key in set(schema.keys()) - set(entry.keys()):
                        description = schema[key]
                        
                        for _, constraint in description[1]:
                            if constraint.get("autoincrement", False):
                                value = randint(0, 2**64)
                                break
                        else:
                            value = None
                            
                        _entry[key] = value

                    yield _entry

            super().extend(filler(iterable))

    def diff(self, other):
        if self.tree.id == other.tree.id:
            return

        if '__schema' in self.keys() and '__schema' not in other.keys():
            yield ('+', {'__schema':self['__schema']})
        elif '__schema' not in self.keys() and '__schema' in other.keys():
            yield ('-', {'__schema'})
        elif '__schema' in self.keys() and '__schema' in other.keys():
            for difference in self['__schema'].diff(other['__schema']):
                yield ('!=', '__schema', *difference)
        
        for difference in super().diff(other):
            match difference:
                case ('+', added):
                    added.pop('__schema')
                    yield ('+', added)
                case ('-', removed):
                    yield ('-', removed - {'__schema'})
                case ('!=', table, *rest):
                    if table != '__schema':
                        yield ('!=', table, *rest)

class Engine(_Engine):
    def __init__(self, tables):
        super().__init__(tables)
        
        if not '__schema' in tables:
            tables['__schema'] = ()
            
    def execute_create(self, statement):
        for entry in self.tables['__schema']:
            if statement.table.name == entry['name']:
                raise ValueError('table {statement.table.name} already exists')
        else:
            self.tables['__schema'].append({'name':statement.table.name,
                                            'description':statement.columns})
            
        super().execute_create(statement)


def __forward(self, method_name, *args, **kwargs):
    if method_name.startswith('execute'):
        statement, = parse(args[0])
        
        return getattr(self._engine, method_name)(*args, *kwargs)
    else:
        return getattr(self._engine, method_name)(*args, *kwargs)

class Cursor:
    def __init__(self, tables):
        self._engine = Engine(tables)

    def __iter__(self):
        yield from iter(self._engine)

    @property
    def description(self):
        return self._engine.description

    def close(self):
        ...

class Connection:
    def __init__(self, path, branch='main'):
        self.__branches = WeakSet()
        
        if path == ':memory:':
            object_store = MemoryObjectStore()
            refs_container = DictRefsContainer({})
        else:
            if not exists(path):
                raise ValueError(f'No such git repositories found at {path}')
            
            if exists(path + '/.git'):
                path += '/.git/'

            object_store = DiskObjectStore(path + '/objects/')
            refs_container = DiskRefsContainer(path + '/')
            
        self.__tables = Vault(object_store, refs_container)

        try:
            self.__tables.checkout(branch)
        except ValueError:
            # init branch if not existing
            self.__tables.commit(branch)
            self.__tables.checkout(branch, True)

        self._engine = Engine(self.__tables)

    def close(self):
        ...

    def commit(self):
        message = f'update at {datetime.now().isoformat()}'
        
        for branch in self.__branches:
            branch.commit(message=message)
            
        if self.__branches:
            self.__tables.merge(self.__branches)
        
        self.__tables.commit(message=(f'merge {self.__tables.ref} with {tuple(branch.ref for branch in self.__branches)}'
                                      if self.__branches
                                      else message))
        
        for branch in self.__branches:
            branch.merge((self.__tables,))

    def rollback(self):
        self.__tables.rollback()

    def cursor(self):
        tables = Vault(self.__tables.object_store,
                       self.__tables.refs,
                       ref=self.__tables.ref)
        
        ref = (tables.ref
               + '_'
               + ''.join(choices(tuple(set(digits)
                                       | set(ascii_letters)),
                                 k=8)))
        tables.checkout(ref, branch=True)
        
        self.__branches.add(tables)
        
        return Cursor(tables)

    @property
    def description(self):
        return self._engine.description

for method_name in {'execute', 'fetchone', 'fetchmany', 'fetchall'}:
    setattr(Cursor, method_name, partialmethod(__forward, method_name))
    setattr(Connection, method_name, partialmethod(__forward, method_name))

def connect(path):
    return Connection(path)
