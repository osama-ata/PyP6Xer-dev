from typing import ClassVar


class ResourceCat:
    obj_list: ClassVar[list] = []

    def __init__(self, params):
        self.rsrc_id = (
            int(params.get("rsrc_id").strip()) if params.get("rsrc_id") else None
        )
        self.rsrc_catg_type_id = (
            int(params.get("rsrc_catg_type_id").strip())
            if params.get("rsrc_catg_type_id")
            else None
        )
        self.rsrc_catg_id = (
            int(params.get("rsrc_catg_type_id").strip())
            if params.get("rsrc_catg_type_id")
            else None
        )
        ResourceCat.obj_list.append(self)

    def get_tsv(self):
        tsv = ["%R", self.rsrc_id, self.rsrc_catg_type_id, self.rsrc_catg_id]
        return tsv

    def get_id(self):
        return self.rsrc_id

    def __repr__(self):
        return self.rsrc_id + " has been assign category " + self.rsrc_catg_id
