from xer_parser.model.classes.taskrsrc import TaskRsrc

__all__ = ["ActivityResources"]


class ActivityResources:
    def __init__(self) -> None:
        self.index = 0
        self._taskrsrc = []

    def add(self, params, data) -> None:  # TODO: Add type annotation for params, data
        self._taskrsrc.append(TaskRsrc(params, data))

    def find_by_id(self, id) -> TaskRsrc:
        obj = list(filter(lambda x: x.taskrsrc_id == id, self._taskrsrc))
        if len(obj) > 0:
            return obj[0]
        return None

    def get_tsv(self) -> list:
        if len(self._taskrsrc) > 0:
            tsv = []
            tsv.append(["%T", "TASKRSRC"])
            tsv.append(
                [
                    "%F",
                    "taskrsrc_id",
                    "task_id",
                    "proj_id",
                    "cost_qty_link_flag",
                    "role_id",
                    "acct_id",
                    "rsrc_id",
                    "pobs_id",
                    "skill_level",
                    "remain_qty",
                    "target_qty",
                    "remain_qty_per_hr",
                    "target_lag_drtn_hr_cnt",
                    "target_qty_per_hr",
                    "act_ot_qty",
                    "act_reg_qty",
                    "relag_drtn_hr_cnt",
                    "ot_factor",
                    "cost_per_qty",
                    "target_cost",
                    "act_reg_cost",
                    "act_ot_cost",
                    "remain_cost",
                    "act_start_date",
                    "act_end_date",
                    "restart_date",
                    "reend_date",
                    "target_start_date",
                    "target_end_date",
                    "rem_late_start_date",
                    "rem_late_end_date",
                    "rollup_dates_flag",
                    "target_crv",
                    "remain_crv",
                    "actual_crv",
                    "ts_pend_act_end_flag",
                    "guid",
                    "rate_type",
                    "act_this_per_cost",
                    "act_this_per_qty",
                    "curv_id",
                    "rsrc_type",
                    "cost_per_qty_source_type",
                    "create_user",
                    "create_date",
                    "cbs_id",
                    "has_rsrchours",
                    "taskrsrc_sum_id",
                ]
            )
            for taskrsrc in self._taskrsrc:
                tsv.append(taskrsrc.get_tsv())
            return tsv
        return []

    def find_by_rsrc_id(self, id) -> TaskRsrc:
        obj = list(filter(lambda x: x.rsrc_id == id, self._taskrsrc))
        return obj

    def find_by_activity_id(self, id):  # TODO: Add correct return type annotation
        obj = list(filter(lambda x: x.task_id == id and x.rsrc_id, self._taskrsrc))
        return obj

    @property
    def count(self) -> int:
        return len(self._taskrsrc)

    def __len__(self) -> int:
        return len(ActivityResources._taskrsrc)

    def __iter__(self) -> "ActivityResources":
        return self

    def __next__(self) -> TaskRsrc:
        if self.index >= len(self._taskrsrc):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._taskrsrc[idx]
