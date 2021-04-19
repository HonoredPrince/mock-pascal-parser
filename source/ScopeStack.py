class ScopeStack:
    '''Stack class for scope management.'''
    def __init__(self):
        self.mark = ['@']
        self._stack = []

    def new_scope(self):
        '''Inserts a scope marking in the stack.'''
        self._stack.append(self.mark)

    def create_id(self, identifier, identifier_type):
        '''Tries to create an identifier.'''
        for i in self._stack[::-1]:
            if i[0] == self.mark:
                break
            if i[0] == identifier:
                raise Exception(
                    'Tried to redefine already existing identifier `{}`.' \
                    .format(identifier)
                    )

        self._stack.append((identifier, identifier_type))

    def search(self, identifier):
        '''Looks for an identifier.'''
        for i in self._stack[::-1]:
            if i[0] == identifier:
                return True
        raise Exception('Identifier `{}` was used before declaration.'.format(identifier))

    def end_scope(self):
        '''Leaves the current scope.'''
        self._stack.reverse()
        self._stack = self._stack[self._stack.index(self.mark)+1:]
        self._stack.reverse()