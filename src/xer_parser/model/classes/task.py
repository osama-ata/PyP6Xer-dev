import locale
from datetime import datetime
from typing import Any, ClassVar

from xer_parser.model.classes.calendar import Calendar
from xer_parser.model.taskprocs import TaskProcs


class Task:
    """
    Represents a Primavera P6 activity/task.

    This class encapsulates all the attributes and functionalities of a Primavera P6 activity,
    including scheduling information, resources, constraints, and relationships.

    Parameters
    ----------
    params : Dict[str, Any]
        Dictionary of parameters from the XER file
    data : Any
        Reference to the main data container

    Attributes
    ----------
    task_id : int
        Unique identifier for the task
    proj_id : int
        Project ID to which this task belongs
    wbs_id : int
        WBS element ID to which this task is assigned
    clndr_id : int
        Calendar ID assigned to this task
    task_code : str
        Short ID which uniquely identifies the task within the project
    task_name : str
        Name of the task
    task_type : str
        Type of task (Task Dependent, Resource Dependent, Level of Effort, etc.)
    duration_type : str
        Duration type (Fixed Units, Fixed Duration, Fixed Units per Time)
    status_code : str
        Current status (Not Started, In Progress, Completed)
    target_drtn_hr_cnt : float
        Original duration in hours
    act_start_date : datetime
        Actual start date of the task
    act_end_date : datetime
        Actual end date of the task
    target_start_date : datetime
        Planned/target start date of the task
    target_end_date : datetime
        Planned/target end date of the task
    cstr_type : str
        Constraint type applied to the task
    total_float_hr_cnt : float
        Total float in hours
    """

    obj_list: ClassVar[list["Task"]] = []

    def __init__(self, params: dict[str, Any], data: Any) -> None:
        """
        Initialize a Task object from XER file parameters.

        Parameters
        ----------
        params : Dict[str, Any]
            Dictionary of parameters from the XER file
        data : Any
            Reference to the main data container
        """
        # Unique ID generated by the system.
        self.task_id = int(params.get("task_id")) if params.get("task_id") else None
        # project to which the activity belongs referenced by system generated unique id
        self.proj_id = int(params.get("proj_id")) if params.get("proj_id") else None
        # wbs element activity assigned to referenced by system unique id
        self.wbs_id = int(params.get("wbs_id")) if params.get("wbs_id") else None
        # calendar assigned to activity referenced by system unique id
        self.clndr_id = int(params.get("clndr_id")) if params.get("clndr_id") else None
        # The physical percent complete can either be user entered or calculated from the activity's weighted steps.
        #  There is a project setting specifying this.
        self.phys_complete_pct = (
            locale.atof(params.get("phys_complete_pct"))
            if "phys_complete_pct" in params
            else None
        )
        # Indicates that the primary resource has sent feedback notes about this activity which have not been
        # reviewed yet.
        self.rev_fdbk_flag = (
            params.get("rev_fdbk_flag") if params.get("rev_fdbk_flag") else None
        )
        # The estimation weight for the activity, used for top-down estimation. Top-down estimation weights are used
        # to calculate the proportion of units that each activity receives in relation to the other activities within
        #  the same WBS. Top-down estimation distributes estimated units in a top-down manner to activities using the
        #  WBS hierarchy.

        self.est_wt = (
            locale.atof(params.get("est_wt").strip())
            if "est_wt" in params and params.get("est_wt") != ""
            else None
        )
        # Indicates that the planned labor and nonlabor units for the activity will not be modified by top-down
        # estimation.
        self.lock_plan_flag = (
            params.get("lock_plan_flag") if params.get("lock_plan_flag") else None
        )
        # Identifies whether the actual and remaining cost for the expense are computed automatically using the
        # planned cost and the activity's schedule percent complete.  If this option is selected,
        # the actual/remaining cost are automatically updated when project actuals are applied.  This assumes the
        # expenses are made according to plan.
        self.auto_compute_act_flag = (
            params.get("auto_compute_act_flag")
            if params.get("auto_compute_act_flag")
            else None
        )
        # The activity percent complete type is one of ""Duration"", ""Units"", or ""Physical"". The percent complete
        #  type controls whether the Activity % Complete is tied to the Duration % Complete, the Units % Complete,
        # or the Physical % Complete for the activity. Set the percent complete type to ""Duration"" for activities
        # which are duration driven, for example, administration tasks and training classes.  Set the percent
        # complete type to ""Physical"" for activities which are work-product driven, for example, creating a
        # document or a product. Set the percent complete type to ""Units"" for activities which are work effort
        # driven, for example, providing a consulting service.
        self.complete_pct_type = (
            params.get("complete_pct_type").strip()
            if params.get("complete_pct_type")
            else None
        )
        # The type of activity, either  'Task Dependent', 'Resource Dependent', 'Level of Effort', 'Start Milestone'
        # or 'Finish Milestone'.   A Task Dependent activity is scheduled using the activity's calendar rather than
        # the calendars of the assigned resources.  A Resource Dependent activity is scheduled using the calendars of
        #  the assigned resources.  This type is used when several resources are assigned to the activity,
        # but they may work separately.  A Start/Finish Milestone is a zero-duration activity, marking a significant
        # start/end of project event. A Level of Effort activity has a duration which is determined by its dependent
        # activities. Administration-type activities are typically level of effort.
        self.task_type = (
            params.get("task_type").strip() if params.get("task_type") else None
        )
        # The duration type of the activity. One of ""Fixed Units per Time"", ""Fixed Duration"", or ""Fixed Units"".
        #   For Fixed Units per Time activities, the resource units per time are constant when the activity duration
        # or units are changed.  This type is used when an activity has fixed resources with fixed productivity
        # output per time period.  For Fixed Duration activities, the activity duration is constant as the units or
        # resource units per time are changed. This type is used when the activity is to be completed within a fixed
        # time period regardless of the resources assigned.  For Fixed Units activities, the activity units are
        # constant when the duration or resource units per time are changed. This type is used when the total amount
        # of work is fixed, and increasing the resources can decrease the activity duration.
        self.duration_type = (
            params.get("duration_type").strip() if params.get("duration_type") else None
        )
        # The current status of the activity, either Not Started, In Progress, or Completed.
        self.status_code = (
            params.get("status_code").strip() if params.get("status_code") else None
        )
        # A short ID which uniquely identifies the activity within the project.
        self.task_code = (
            params.get("task_code").strip() if params.get("task_code") else None
        )
        # The name of the activity. The activity name does not have to be unique.
        self.task_name = (
            params.get("task_name").strip() if params.get("task_name") else None
        )
        # Resource ID Name
        self.rsrc_id = (
            int(params.get("rsrc_id").strip()) if params.get("rsrc_id") else None
        )
        # The amount of time the wbs can be delayed before delaying the project finish date. Total int can be
        # computed as Late Start - Early Start or as Late Finish - Early Finish; this option can be set when running
        # the project scheduler.
        self.total_float_hr_cnt = (
            locale.atof(params.get("total_float_hr_cnt").strip())
            if params.get("total_float_hr_cnt")
            and params.get("total_float_hr_cnt") != ""
            else None
        )
        # The amount of time the activity can be delayed before delaying the start
        # date of any successor activity.
        self.free_float_hr_cnt = (
            locale.atof(params.get("free_float_hr_cnt"))
            if params.get("free_float_hr_cnt")
            else None
        )
        # Remaining duration is the total working time from the activity remaining start date to the remaining finish
        #  date. The remaining working time is computed using the activity's calendar. Before the activity is
        # started, the remaining duration is the same as the Original Duration. After the activity is completed the
        # remaining duration is zero.
        self.remain_drtn_hr_cnt = (
            locale.atof(params.get("remain_drtn_hr_cnt").strip())
            if params.get("remain_drtn_hr_cnt")
            else 0
        )
        # The total actual labor units for all child activities
        self.act_work_qty = (
            locale.atof(params.get("act_work_qty"))
            if params.get("act_work_qty")
            else None
        )
        # The remaining units for all labor resources assigned to the activity. The remaining units reflects the work
        #  remaining to be done for the activity. Before the activity is started, the remaining units are the same as
        #  the planned units. After the activity is completed, the remaining units are zero.
        self.remain_work_qty = (
            locale.atof(params.get("remain_work_qty"))
            if params.get("remain_work_qty")
            else None
        )
        # The planned units for all labor resources assigned to the activity.
        self.target_work_qty = (
            locale.atof(params.get("target_work_qty"))
            if params.get("target_work_qty")
            else None
        )
        # Original Duration is the planned working time for the resource assignment on the activity,
        # from the resource's planned start date to the planned finish date. The planned working time is computed
        # using the calendar determined by the Activity Type. Resource Dependent activities use the resource's
        # calendar; other activity types use the activity's calendar. This is the duration that Timesheets users
        # follow and the schedule variance is measured against.
        self.target_drtn_hr_cnt = (
            locale.atof(params.get("target_drtn_hr_cnt").strip())
            if params.get("target_drtn_hr_cnt")
            else None
        )
        # The planned units for all nonlabor resources assigned to the activity.
        self.target_equip_qty = (
            locale.atof(params.get("target_equip_qty"))
            if params.get("target_equip_qty")
            else None
        )
        # The actual units for all nonlabor resources assigned to the activities under the WBS.
        self.act_equip_qty = (
            locale.atof(params.get("act_equip_qty"))
            if params.get("act_equip_qty")
            else None
        )
        # The remaining units for all nonlabor resources assigned to the activity. The remaining units reflects the
        # work remaining to be done for the activity.  Before the activity is started, the remaining units are the
        # same as the planned units. After the activity is completed, the remaining units are zero.
        self.remain_equip_qty = (
            locale.atof(params.get("remain_equip_qty"))
            if params.get("remain_equip_qty")
            else None
        )
        # The constraint date for the activity, if the activity has a constraint. The activity's constraint type
        # determines whether this is a start date or finish date.  Activity constraints are used by the project
        # scheduler.
        self.cstr_date = (
            datetime.strptime(params.get("cstr_date"), "%Y-%m-%d %H:%M")
            if params.get("cstr_date")
            else None
        )
        # The date on which the activity is actually started.
        self.act_start_date = (
            datetime.strptime(params.get("act_start_date"), "%Y-%m-%d %H:%M")
            if params.get("act_start_date")
            else None
        )
        # The date on which the activity is actually finished.
        self.act_end_date = (
            datetime.strptime(params.get("act_end_date"), "%Y-%m-%d %H:%M")
            if params.get("act_end_date")
            else None
        )
        # the activity late start date
        self.late_start_date = (
            datetime.strptime(params.get("late_start_date"), "%Y-%m-%d %H:%M")
            if params.get("late_start_date")
            else None
        )
        # The latest possible date the activity must finish without delaying the project finish date. This date is
        # computed by the project scheduler based on network logic, schedule
        # constraints, and resource availability.
        self.late_end_date = (
            datetime.strptime(params.get("late_end_date"), "%Y-%m-%d %H:%M")
            if params.get("late_end_date")
            else None
        )
        # The date the activity is expected to be finished according to the progress made on the activity's work
        # products. The expected finish date is entered manually by people familiar with progress of the activity's
        # work products.
        self.expect_end_date = (
            datetime.strptime(params.get("expect_end_date"), "%Y-%m-%d %H:%M")
            if params.get("expect_end_date")
            else None
        )
        # The earliest possible date the remaining work for the activity can begin. This date is computed by the
        # project scheduler based on network logic, schedule constraints, and resource availability.
        self.early_start_date = (
            datetime.strptime(params.get("early_start_date"), "%Y-%m-%d %H:%M")
            if params.get("early_start_date")
            else None
        )
        # The earliest possible date the activity can finish. This date is computed by the project scheduler based on
        #  network logic, schedule constraints, and resource availability.
        self.early_end_date = (
            datetime.strptime(params.get("early_end_date"), "%Y-%m-%d %H:%M")
            if params.get("early_end_date")
            else None
        )
        # The date the remaining work for the activity is scheduled to begin. This date is computed by the project
        # scheduler but can be updated manually by the project manager.  Before the activity is started,
        # the remaining start date is the same as the planned start date.  This is the start date that Timesheets
        # users follow.
        self.restart_date = (
            datetime.strptime(params.get("restart_date"), "%Y-%m-%d %H:%M")
            if params.get("restart_date")
            else None
        )
        # The date the remaining work for the activity is scheduled to finish. This date is computed by the project
        # scheduler but can be updated manually by the project manager. Before the activity is started, the remaining
        # finish date is the same as the planned finish date.  This is the finish
        # date that Timesheets users follow.
        self.reend_date = (
            datetime.strptime(params.get("reend_date"), "%Y-%m-%d %H:%M")
            if params.get("reend_date")
            else None
        )
        # The date the activity is scheduled to begin. This date is computed by the project scheduler but can be
        # updated manually by the project manager. This date is not changed by the project scheduler after the
        # activity has been started.
        self.target_start_date = (
            datetime.strptime(params.get("target_start_date"), "%Y-%m-%d %H:%M")
            if params.get("target_start_date")
            else None
        )
        # The date the activity is scheduled to finish. This date is computed by the project scheduler but can be
        # updated manually by the project manager.  This date is not changed by the project scheduler after the
        # activity has been started.
        self.target_end_date = (
            datetime.strptime(params.get("target_end_date"), "%Y-%m-%d %H:%M")
            if params.get("target_end_date")
            else None
        )
        # Remaining late start date is calculated by the scheduler.
        self.rem_late_start_date = (
            datetime.strptime(params.get("rem_late_start_date"), "%Y-%m-%d %H:%M")
            if params.get("rem_late_start_date")
            else None
        )
        # Remaining late end date is calculated by the scheduler.
        self.rem_late_end_date = (
            datetime.strptime(params.get("rem_late_end_date"), "%Y-%m-%d %H:%M")
            if params.get("rem_late_end_date")
            else None
        )
        # The type of constraint applied to the activity start or finish date. Activity constraints are used by the
        # project scheduler.  Start date constraints are 'Start On', 'Start On or Before', 'Start On or After' and
        # 'Mandatory Start'.  Finish date constraints are 'Finish On', 'Finish On or Before', 'Finish On or After'
        # and 'Mandatory Finish'.  Another type of constraint, 'As Late as Possible', schedules the activity as late
        # as possible based on the available free int.
        self.cstr_type = (
            params.get("cstr_type").strip() if params.get("cstr_type") else None
        )
        self.priority_type = (
            params.get("priority_type").strip() if params.get("priority_type") else None
        )
        # The date progress is suspended on an activity.
        self.suspend_date = (
            datetime.strptime(params.get("suspend_date").strip(), "%Y-%m-%d %H:%M")
            if params.get("suspend_date")
            else None
        )
        # The date progress is resumed on an activity.
        self.resume_date = (
            datetime.strptime(params.get("resume_date").strip(), "%Y-%m-%d %H:%M")
            if params.get("resume_date")
            else None
        )
        self.int_path = (
            params.get("int_path").strip() if params.get("int_path") else None
        )
        # This field is computed by the project scheduler and identifies the order in which the activities were
        # processed within the int path.
        self.int_path_order = (
            params.get("int_path_order").strip()
            if params.get("int_path_order")
            else None
        )
        self.guid = params.get("guid").strip() if params.get("guid") else None
        self.tmpl_guid = (
            params.get("tmpl_guid").strip() if params.get("tmpl_guid") else None
        )
        # The second constraint date for the activity, if the activity has a constraint.
        self.cstr_date2 = (
            datetime.strptime(params.get("cstr_date2"), "%Y-%m-%d %H:%M")
            if params.get("cstr_date2")
            else None
        )
        # The second type of constraint applied to the activity start or finish date.
        self.cstr_type2 = (
            params.get("cstr_type2").strip() if params.get("cstr_type2") else None
        )
        self.driving_path_flag = (
            params.get("driving_path_flag") if params.get("driving_path_flag") else None
        )
        # The actual this period units for all labor resources assigned to the activity.
        self.act_this_per_work_qty = (
            locale.atof(params.get("act_this_per_work_qty"))
            if params.get("act_this_per_work_qty")
            else None
        )
        # The actual this period units for all nonlabor resources assigned to the activity.
        self.act_this_per_equip_qty = (
            locale.atof(params.get("act_this_per_equip_qty"))
            if params.get("act_this_per_equip_qty")
            else None
        )
        # The External Early Start date is the date the external relationship was scheduled to finish.  This date may
        #  be used to calculate the start date of the current activity during scheduling.  This field is populated on
        #  import when an external relationship is lost.
        try:
            self.external_early_start_date = (
                datetime.strptime(
                    params.get("external_early_start_date").strip(), "%Y-%m-%d %H:%M"
                )
                if params.get("external_early_start_date")
                else None
            )
            self.external_late_end_date = (
                datetime.strptime(
                    params.get("external_late_end_date"), "%Y-%m-%d %H:%M"
                )
                if params.get("external_late_end_date")
                else None
            )
        except BaseException:
            pass
        self.create_date = (
            datetime.strptime(params.get("create_date"), "%Y-%m-%d %H:%M")
            if params.get("create_date")
            else None
        )
        self.update_date = (
            datetime.strptime(params.get("update_date"), "%Y-%m-%d %H:%M")
            if params.get("update_date")
            else None
        )
        self.create_user = (
            params.get("create_user").strip() if params.get("create_user") else None
        )
        self.update_user = (
            params.get("update_user").strip() if params.get("update_user") else None
        )
        self.location_id = (
            params.get("location_id").strip() if params.get("location_id") else None
        )
        self.calendar = Calendar.find_by_id(self.clndr_id)
        # self.wbs = WBS.find_by_id(int(self.wbs_id) if self.wbs_id else None)
        # Task.obj_list.append(self)
        self.data = data
        self.logic_missing = False  # Initialize logic_missing attribute

    def get_tsv(self) -> list[Any]:
        """
        Get the task data in TSV format.

        Returns
        -------
        List[Any]
            Task data formatted for TSV output
        """
        return [
            "%R",
            self.task_id,
            self.proj_id,
            self.wbs_id,
            self.clndr_id,
            self.phys_complete_pct,
            self.rev_fdbk_flag,
            self.est_wt,
            self.lock_plan_flag,
            self.auto_compute_act_flag,
            self.complete_pct_type,
            self.task_type,
            self.duration_type,
            self.status_code,
            self.task_code,
            self.task_name,
            self.rsrc_id,
            self.total_float_hr_cnt,
            self.free_float_hr_cnt,
            self.remain_drtn_hr_cnt,
            self.act_work_qty,
            self.remain_work_qty,
            self.target_work_qty,
            self.target_drtn_hr_cnt,
            self.target_equip_qty,
            self.act_equip_qty,
            self.remain_equip_qty,
            self.cstr_date.strftime("%Y-%m-%d %H:%M") if self.cstr_date else None,
            (
                self.act_start_date.strftime("%Y-%m-%d %H:%M")
                if self.act_start_date
                else None
            ),
            self.act_end_date.strftime("%Y-%m-%d %H:%M") if self.act_end_date else None,
            (
                self.late_start_date.strftime("%Y-%m-%d %H:%M")
                if self.late_start_date
                else None
            ),
            (
                self.late_end_date.strftime("%Y-%m-%d %H:%M")
                if self.late_end_date
                else None
            ),
            (
                self.expect_end_date.strftime("%Y-%m-%d %H:%M")
                if self.expect_end_date
                else None
            ),
            (
                self.early_start_date.strftime("%Y-%m-%d %H:%M")
                if self.early_start_date
                else None
            ),
            (
                self.early_end_date.strftime("%Y-%m-%d %H:%M")
                if self.early_end_date
                else None
            ),
            self.restart_date.strftime("%Y-%m-%d %H:%M") if self.restart_date else None,
            self.reend_date.strftime("%Y-%m-%d %H:%M") if self.reend_date else None,
            (
                self.target_start_date.strftime("%Y-%m-%d %H:%M")
                if self.target_start_date
                else None
            ),
            (
                self.target_end_date.strftime("%Y-%m-%d %H:%M")
                if self.target_end_date
                else None
            ),
            (
                self.rem_late_start_date.strftime("%Y-%m-%d %H:%M")
                if self.rem_late_start_date
                else None
            ),
            (
                self.rem_late_end_date.strftime("%Y-%m-%d %H:%M")
                if self.rem_late_end_date
                else None
            ),
            self.cstr_type,
            self.priority_type,
            self.suspend_date.strftime("%Y-%m-%d %H:%M") if self.suspend_date else None,
            self.resume_date.strftime("%Y-%m-%d %H:%M") if self.resume_date else None,
            self.int_path,
            self.int_path_order,
            self.guid,
            self.tmpl_guid,
            self.cstr_date2.strftime("%Y-%m-%d %H:%M") if self.cstr_date2 else None,
            self.cstr_type2,
            self.driving_path_flag,
            self.act_this_per_work_qty,
            self.act_this_per_equip_qty,
            (
                self.external_early_start_date.strftime("%Y-%m-%d %H:%M")
                if self.external_early_start_date
                else None
            ),
            (
                self.external_late_end_date.strftime("%Y-%m-%d %H:%M")
                if self.external_late_end_date
                else None
            ),
            self.create_date.strftime("%Y-%m-%d %H:%M") if self.create_date else None,
            self.update_date.strftime("%Y-%m-%d %H:%M") if self.update_date else None,
            self.create_user,
            self.update_user,
            self.location_id,
        ]

    @property
    def id(self) -> int:
        """
        Get the task ID.

        Returns
        -------
        int
            The unique identifier for this task
        """
        return self.task_id

    @property
    def totalint(self) -> float | None:
        """
        Get the total float in days.

        Returns
        -------
        float or None
            Total float in days (8 hours per day), or None if not available
        """
        if self.total_int_hr_cnt:
            tf = int(self.total_int_hr_cnt) / 8.0
        else:
            return None
        return tf

    @property
    def resources(self) -> list[Any]:
        """
        Get all resources assigned to this task.

        Returns
        -------
        List[Any]
            List of TaskRsrc objects assigned to this task
        """
        return self.data.taskresource.find_by_activity_id(self.task_id)

    @property
    def steps(self) -> list[Any]:
        """
        Get all steps (work products) for this task.

        Returns
        -------
        List[Any]
            List of TaskProc objects belonging to this task
        """
        return TaskProcs.find_by_activity_id(self.task_id)

    @property
    def activitycodes(self) -> list[Any]:
        """
        Get all activity codes assigned to this task.

        Returns
        -------
        List[Any]
            List of TaskActv objects assigned to this task
        """
        return self.data.taskactvcodes.find_by_activity_id(self.task_id)

    @property
    def duration(self) -> float:
        """
        Get the duration of the task in days.

        Returns
        -------
        float
            Duration in days (calculated from hours based on calendar working hours)
        """
        dur = None
        if self.target_drtn_hr_cnt:
            if self.calendar.day_hr_cnt:
                dur = self.target_drtn_hr_cnt / self.calendar.day_hr_cnt
            else:
                dur = self.target_drtn_hr_cnt / 8.0
        else:
            dur = 0.0
        return dur

    @property
    def constraints(self) -> dict[str, Any] | None:
        """
        Get the constraints applied to this task.

        Returns
        -------
        Dict[str, Any] or None
            Dictionary with constraint type and date, or None if no constraints
        """
        if self.cstr_type is None or self.cstr_date is None:
            return None
        return {"ConstraintType": self.cstr_type, "ConstrintDate": self.cstr_date}

    @property
    def start_date(self) -> datetime | None:
        """
        Get the effective start date of the task.

        Returns the actual start date if the task has started, otherwise the target start date.

        Returns
        -------
        datetime or None
            The effective start date of the task
        """
        if self.act_start_date:
            return self.act_start_date
        return self.target_start_date

    @property
    def end_date(self) -> datetime | None:
        """
        Get the effective end date of the task.

        Returns the actual end date if the task has finished, otherwise the target end date.

        Returns
        -------
        datetime or None
            The effective end date of the task
        """
        if self.act_end_date:
            return self.act_end_date
        return self.target_end_date

    @property
    def successors(self) -> list[Any]:
        """
        Get all successor tasks to this task.

        Returns
        -------
        List[Any]
            List of tasks that are successors to this task
        """
        return self.data.predecessors.get_successors(self.task_id)

    @property
    def predecessors(self) -> list[Any]:
        """
        Get all predecessor tasks to this task.

        Returns
        -------
        List[Any]
            List of tasks that are predecessors to this task
        """
        return self.data.predecessors.get_predecessors(self.task_id)

    @classmethod
    def find_by_wbs_id(cls, wbs_id: int) -> list["Task"]:
        """
        Find all tasks belonging to a WBS element.

        Parameters
        ----------
        wbs_id : int
            The ID of the WBS element

        Returns
        -------
        List[Task]
            List of tasks belonging to the specified WBS element
        """
        return [v for v in cls.obj_list if v.wbs_id == wbs_id]

    def __repr__(self) -> str:
        """
        String representation of the task.

        Returns
        -------
        str
            The task's code
        """
        return self.task_code
