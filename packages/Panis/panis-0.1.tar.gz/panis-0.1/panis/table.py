# -*- coding: utf-8 -*-

import pandas as pd
import datetime 

class Table():
    def __init__(self, 
                 conn, 
                 name, 
                 columns):
        self.conn = conn
        self.name = name
        self.columns = columns
        
        # if the table does not exist, create it
        if not self._check_if_table_exists(name=self.name):
            print('table '+self.name+' does not exist. Creation...')
            self.create_table()
        
        # if a column is missing, complete the table
        self.complete_columns()
    
    def create_table(self):
            lines = []
            for col in self.columns:
                lines.append(col.sql_def())
            
            for col in self.columns:
                ref = col.sql_references()
                if ref is not None:
                    lines.append(ref)
                    
            query = "CREATE TABLE "+self.name+"("
            query += ", ".join(lines)
            query += ")"
            
            self._commit(query)
            
    def complete_columns(self):
        table_columns = self.get_columns()
        for column in self.columns:
            if column.name not in table_columns:
                query = "ALTER TABLE "+self.name
                query += " ADD "
                query += column.sql_def()
                
                if column.references is not None:
                    query += " "
                    query += column.sql_references(alter=True)
                
                self._commit(query)
    
    def insert_entry(self, table_name=None, **data):
        """
        Insert entry into a table. data is a dict with table columns as keys.
        
        Parameters
        ----------
        table : TYPE
            DESCRIPTION.
        **data : kwargs
            kwargs of column=values
            

        Returns
        -------
        i : int
            index of the entry

        """
        
        if table_name is None:
            table_name = self.name
        
        self._check_data(data=data)
        
        query = "INSERT INTO "+table_name
        if len(data.keys()) > 0:
            query += " (" + ", ".join(data.keys()) + ")"
            query += " VALUES("
            query += ", ".join([str(v) for v in data.values()])
            query += ")"
        else:
            query += " DEFAULT VALUES"
                
        self._commit(query = query)
        
        i = self._tuples(query="SELECT id FROM "+table_name+" ORDER BY id DESC LIMIT 1")[0][0]
        return i
    
    def delete_entry(self, i):
        """
        remove entry

        Parameters
        ----------
        table : str
            table name
        
        i : int
            entry index.
        
        Returns
        -------
        None.

        """
        query = "DELETE FROM "
        query += self.name+" WHERE "
        query += "id='"+str(i)+"'"
        
        self._commit(query=query)
    
    def delete(self, where):
        query = "DELETE FROM "
        query += self.name+" WHERE "
        query += where
        
        self._commit(query=query)
    
    def purge(self, confirm='no'):
        query = "DELETE FROM "+self.name
        if confirm == 'yes':
            self._commit(query=query)
    
    def update_entry(self, i, id_column='id', **data):
        """
        Parameters
        ----------
        table : str
            table name
        i : int
            entry index.
        id_column : str, default='id'
            index column name
        **data : kwargs
            kwargs of column=values
        """
        
        self._check_data(data)
        
        query = "UPDATE "+self.name
        query += " SET "
        query += ", ".join([k+"="+str(v) for k, v in data.items()])
        query += " WHERE "+id_column+"='"+str(i)+"'"
        
        self._commit(query=query)
        
    def get_entry(self, i, columns=None, table_name=None):
        """
        Parameters
        ----------
        table : str
            table name
        i : int
            entry index.
        columns : list(str), default=None
            list of column names. If None, "all columns" is set.

        Returns
        -------
        data : dict
            dict of data (keys are sql columns).

        """
        if columns is None:
            columns = self.get_columns()
            
        if table_name is None:
            table_name = self.name
        
        query = "SELECT "+", ".join(columns)
        query += " FROM "+table_name
        query += " WHERE id="+str(i)
        query += " LIMIT 1"
        
        r = self._fetchone(query=query)
        
        if r is None:
            return None
        
        d = {c : r[i] for i, c in enumerate(columns)}
        
        return d
    
    def get_entries(self, columns=None, where=None, order_by=None, desc=None, list_dict=False, pandas=False, table_name=None):
        """
        Parameters
        ----------
        desc is obsolete
        
        table : str
            table name
        columns : list(str), default=None
            list of column names. If None, "all columns" is set.
        where : str, default=None
            where condition
        order_by : str, default=None
            order by condition

        Returns
        -------
        t : tuples(list(data))
            returned data
        """
        if columns is None:
            columns = self.get_columns()
        
        if table_name is None:
            table_name = self.name
        
        query = "SELECT "+", ".join(columns)
        query += " FROM "+table_name
        if where is not None:
            query += " WHERE "+where
        if order_by is not None:
            query += " ORDER BY "+order_by
        
        tup = self._tuples(query=query)
        
        if list_dict:
            return [{c : t[i] for i, c in enumerate(columns)} for t in tup]
        
        if pandas:
            return self._pandas(query=query, columns=columns)
        
        return tup
    
    def get_columns(self, table_name=None):
        """
        Parameters
        ----------
        table : str
            table name

        Returns
        -------
        columns : list(str)
            list of columns.

        """
        if table_name is None:
            table_name = self.name
        
        pragma = self._tuples(query="PRAGMA table_info("+table_name+")")
        return [p[1] for p in pragma]
    
    def _select_data(self, data, table_name=None):
        if table_name is None:
            table_name = self.name
        
        columns = self.get_columns(table_name=table_name)
        
        selected_data = {}
        for k, v in data.items():
            if k in columns:
                selected_data[k] = v
        
        return selected_data

    def _magic_quotes(self, s):
        return s.replace("'", "''")

    def _check_if_table_exists(self, name):
        query = """
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' 
        AND name='"""+name+"""'
        """
        
        r = self._fetchone(query)
        
        if r is not None:
            return True
        return False
    
    def _fetchone(self, query):
        print(query)
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchone()
    
    def _tuples(self, query):
        print(query)
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    def _tuples_dict(self, query, columns):
        tup = self._tuples(query)
        
        return [{c : t[i] for i, c in enumerate(columns)} for t in tup]
    
    def _pandas(self, query, columns=None):
        print(query)
        df = pd.read_sql_query(query, self.conn)
        
        if columns is not None:
            df.columns = columns
        return df
    
    def _commit(self, query, var=None):
        print(query)
        
        cursor = self.conn.cursor()
        if var is None:
            cursor.execute(query)
        else:
            cursor.execute(query, var)
        self.conn.commit()
    
    def _commit_script(self, query_script):
        print(query_script)
        cursor = self.conn.cursor()
        cursor.executescript(query_script)
        self.conn.commit()
        
    
    def _check_data(self, data):
        self._check_string(data=data)
        self._check_boolean(data=data)
        self._check_none(data=data)
    
    def _check_boolean(self, data):
        for k, v in data.items():
            if type(v) is bool:
                data[k] = int(v)
    
    def _check_none(self, data):
        for k, v in data.items():
            if v is None:
                data[k] = 'NULL'
    
    def _check_string(self, data):
        for k, v in data.items():
            if type(v) is str:
                data[k] = "'"+self._magic_quotes(v)+"'"
        
class Column():
    def __init__(self, 
                 name, 
                 sql_type,
                 index=False,
                 default=None, 
                 references=None, 
                 on_update='NO ACTION',
                 on_delete='NO ACTION'):
        """
                     

        Parameters
        ----------
        index : BOOL, default=False
            if True, autoincremented index
        default : TYPE, optional
            DESCRIPTION. The default is None.
        references : tuple(str), default=None
            If None, no references. Tuple corresponds to (table, column).
        on_update : {'SET NULL','SET DEFAULT','RESTRICT','NO ACTION','CASCADE'}, default='NO ACTION'
            action on reference update.
        on_delete : {'SET NULL','SET DEFAULT','RESTRICT','NO ACTION','CASCADE'}, default='NO ACTION'
            action on reference delete.
        """
        
        self.name = name
        self.sql_type = sql_type
        self.index = index
        self.default = default
        self.references = references
        self.on_update = on_update
        self.on_delete = on_delete
    
    def sql_def(self):
        c = [self.name]
        c.append(self.sql_type)
        if self.index:
            c.append("PRIMARY KEY AUTOINCREMENT UNIQUE")
        if self.default is not None:
            default = self.default
            if default=='':
                default = "''"
            c.append("DEFAULT "+str(default))
        
        return " ".join(c)
    
    def sql_references(self, alter=False):
        if self.references is None:
            return None
        
        if not alter:
            s = ["FOREIGN KEY"]
            s.append("("+self.name+")")
            s.append("REFERENCES")
        else:
            s = ["REFERENCES"]
        s.append(self.references[0])
        s.append("("+self.references[1]+")")
        s.append("ON UPDATE "+self.on_update)
        s.append("ON DELETE "+self.on_delete)
        
        return " ".join(s)

def date_to_timestamp(a, date_format ='%d/%m/%Y'):
    return datetime.datetime.strptime(a, date_format).timestamp()
    
def timestamp_to_date(d, date_format ='%d/%m/%Y'):
    return datetime.datetime.fromtimestamp(d).strftime(date_format)

def today():
    return int(datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    # return datetime.datetime.today().timestamp()