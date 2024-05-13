# -*- coding: utf-8 -*-

from .meetingsubject import MeetingSubject
from .meetingsubjectlog import MeetingSubjectLog

class Cooperation():
    def __init__(self, conn, farm):
        self.meetingsubject = MeetingSubject(conn=conn, farm=farm)
        self.meetingsubjectlog = MeetingSubjectLog(conn=conn, farm=farm)
