# -*- coding: utf-8 -*-

from ..table import Table, Column

class MeetingSubjectLog(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'cooperation_meetingsubjectlog'
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='cooperation_meetingsubject_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('cooperation_meetingsubject','id'),
                          on_update='CASCADE',
                          on_delete='CASCADE'),
                   Column(name='date',
                          sql_type='INTEGER',
                          default=0),
                   ]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)