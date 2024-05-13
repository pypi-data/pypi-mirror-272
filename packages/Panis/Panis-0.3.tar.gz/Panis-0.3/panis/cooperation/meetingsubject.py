# -*- coding: utf-8 -*-

from ..table import Table, Column, today

class MeetingSubject(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'cooperation_meetingsubject'
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='name',
                          sql_type='TEXT',
                          default=''),
                   Column(name='state',
                          sql_type='INT',
                          default=1),
                   Column(name='kind',
                          sql_type='INT',
                          default=1),
                   Column(name='creator',
                          sql_type='TEXT',
                          default=''),
                   Column(name='deadline',
                          sql_type='INT',
                          default=0),
                   Column(name='log',
                          sql_type='TEXT',
                          default=''),
                   Column(name='next_agenda',
                          sql_type='BOOLEAN',
                          default=0),
                   Column(name='position',
                          sql_type='INT',
                          default='NULL'),
                   Column(name='note',
                          sql_type='TEXT',
                          default=''),
                   Column(name='duration',
                          sql_type='INT',
                          default=10)
                   ]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)

    def purge_next_agenda(self):
        query = "UPDATE "+self.name
        query += " SET next_agenda=0"
        
        self._commit(query=query)
    
    def get_filtered_entries(self,
                             state_list=[],
                             next_agenda=False,
                             log_date_operator="<=",
                             log_date=today()):
        
        where = ""
        
        if len(state_list)>0:
            where += " state IN (" + ', '.join(state_list) + ')'
        
        if next_agenda:
            where += " AND next_agenda="+str(int(next_agenda))
        
        query = """
        SELECT 
        cooperation_meetingsubject.id,
        cooperation_meetingsubject.name,
        cooperation_meetingsubject.kind,
        cooperation_meetingsubject.state,
        cooperation_meetingsubject.deadline,
        cooperation_meetingsubject.position,
        cooperation_meetingsubject.duration,
        cooperation_meetingsubject.next_agenda
        FROM
        cooperation_meetingsubject
        WHERE """+where+"""
        ORDER BY
        cooperation_meetingsubject.state, 
        cooperation_meetingsubject.deadline ASC, 
        cooperation_meetingsubject.kind, 
        cooperation_meetingsubject.name
        """
        
        columns_subjects = ['id',
                   'name', 
                   'kind',
                   'state',
                   'deadline',
                   'position',
                   'duration',
                   'next_agenda']
        
        subjects =  self._pandas(query,
                                 columns=columns_subjects)
        
        if log_date_operator == 'X':
            return subjects
        
        query = """
        SELECT
        cooperation_meetingsubject_id,
        date
        FROM
        cooperation_meetingsubjectlog
        WHERE
        date """+log_date_operator+str(log_date)+"""
        """
        columns_log = ['id',
                   'log_date']
        
        logs = self._pandas(query,
                            columns=columns_log)
        
        subjects = subjects.merge(logs,
                                  how='inner',
                                  on='id')
        subjects[columns_subjects].drop_duplicates(inplace=True)
        
        return subjects