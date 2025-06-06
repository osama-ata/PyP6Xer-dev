import locale
from typing import ClassVar

from xer_parser.model.classes.calendar_data import CalendarData


class Calendar:
    obj_list: ClassVar[list] = []

    def __init__(self, params):
        # Unique ID generated by the system.
        self.clndr_id = (
            int(params.get("clndr_id").strip()) if params.get("clndr_id") else None
        )
        # Identifies the default global calendar (applies to global calendars only).
        self.default_flag = (
            params.get("default_flag").strip() if params.get("default_flag") else None
        )
        # The name of the calendar.
        self.clndr_name = (
            params.get("clndr_name").strip() if params.get("clndr_name") else None
        )
        self.proj_id = params.get("proj_id").strip() if params.get("proj_id") else None
        # The global calendar to which this calendar is linked.  Any changes to the global calendar are automatically
        #  propagated to this calendar.
        self.base_clndr_id = (
            params.get("base_clndr_id").strip() if params.get("base_clndr_id") else None
        )
        # Date of last changes to calendar.
        self.last_chng_date = (
            params.get("last_chng_date").strip()
            if params.get("last_chng_date")
            else None
        )
        # The calendar type - either global, resource, or project. Global calendars can be assigned to projects and
        # resources. Resource calendars can be assigned only to resources. Project
        # calendars are specific to projects.
        self.clndr_type = (
            params.get("clndr_type").strip() if params.get("clndr_type") else None
        )
        # The number of work hours per day. This conversion factor is used for displaying time units and durations in
        self.day_hr_cnt = (
            locale.atof(params.get("day_hr_cnt")) if params.get("day_hr_cnt") else None
        )
        # The number of work hours per week. This conversion factor is used for displaying time units and durations
        # in the user's selected display formats.
        self.week_hr_cnt = (
            locale.atof(params.get("week_hr_cnt"))
            if params.get("week_hr_cnt")
            else None
        )
        # The number of work hours per month. This conversion factor is used for displaying time units and durations
        # in the user's selected display formats.
        self.month_hr_cnt = (
            locale.atof(params.get("month_hr_cnt"))
            if params.get("month_hr_cnt")
            else None
        )
        # The number of work hours per year. This conversion factor is used for displaying time units and durations
        # in the user's selected display formats.
        self.year_hr_cnt = (
            locale.atof(params.get("year_hr_cnt"))
            if params.get("year_hr_cnt")
            else None
        )
        self.rsrc_private = (
            params.get("rsrc_private").strip() if params.get("rsrc_private") else None
        )
        self.clndr_data = (
            params.get("clndr_data").strip() if params.get("clndr_data") else None
        )
        self.working_days = {}
        self.exceptions = []

        if self.clndr_data:
            c = CalendarData(self.clndr_data)
            self.working_days = c.get_days()
            self.working_hours = c.get_work_pattern()
            self.exceptions = c.get_exceptions()

        Calendar.obj_list.append(self)

    def get_tsv(self):
        return [
            "%R",
            self.clndr_id,
            self.default_flag,
            self.clndr_name,
            self.proj_id,
            self.base_clndr_id,
            self.last_chng_date,
            self.clndr_type,
            self.day_hr_cnt,
            self.week_hr_cnt,
            self.month_hr_cnt,
            self.year_hr_cnt,
            self.rsrc_private,
            self.clndr_data,
        ]

    @staticmethod
    def find_by_id(id):
        obj = list(filter(lambda x: x.clndr_id == id, Calendar.obj_list))
        return obj[0] if obj else None

    def __repr__(self):
        return f"{self.clndr_name} : {self.day_hr_cnt}\n{self.clndr_data}"
