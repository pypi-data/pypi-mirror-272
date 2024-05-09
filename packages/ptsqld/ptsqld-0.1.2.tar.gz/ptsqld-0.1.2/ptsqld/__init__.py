from os.path import exists
from datetime import datetime
from sqlton import parse
from sqlton.ast import Select
from sqletic import Engine as _Engine
from functools import partialmethod
from echovault import Vault 
from dulwich.object_store import DiskObjectStore, MemoryObjectStore
from dulwich.refs import DiskRefsContainer, DictRefsContainer
from random import choices
from string import ascii_letters, digits
from weakref import WeakSet

class Engine(_Engine):
    def __init__(self, tables):
        super().__init__(tables)
        self.__schema = {}
        
    def execute_create(self, statement):
        self.__schema = {statement.table.name:statement.columns}
        super().execute_create(statement)

    def execute_insert(self, statement):
        # TODO
        # if All() get the column from self.__schema[table.name]
        # elif columns and some are missing fill with information from schema
        super().execute(statement)

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
