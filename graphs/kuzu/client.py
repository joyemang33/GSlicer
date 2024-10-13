import kuzu

class KuzuClient:
    def __init__(self, name = './graphs/kuzu/data/test'):
        '''
        connect to database with 'name'
        create the database if does not exist
        '''
        self.enable_print = False
        self.db = kuzu.Database(name)
        self.conn = kuzu.Connection(self.db)

    def run(self, stmt):
        '''
        run the cypher query
        '''
        if self.enable_print: print(stmt)
        return self.conn.execute(stmt)
