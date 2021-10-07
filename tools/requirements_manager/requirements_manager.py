import json
from typing import Optional
from jsonschema import validate

REQUIREMENTS_FILE = "requirements.json"
REQUIREMENTS_SCHEMA_FILE = "tools/requirements_manager/schema_requirements.json"


class RequirementsManager:
    _req_data: list
    _req_schema: dict
    _next_id: int

    def __init__(self):
        with open(REQUIREMENTS_SCHEMA_FILE, "r") as file_h:
            self._req_schema = json.load(file_h)
        self._load_data()

    def __del__(self):
        self._safe_data()

    def _validate_data(self, data: dict):
        validate(data, self._req_schema)

    def _get_save_data(self) -> dict:
        return {"requirements": self._req_data,
                "settings": {
                    "next_id": self._next_id
                }}

    def _load_data(self):
        self._req_data = []
        self._next_id = 0
        try:
            with open(REQUIREMENTS_FILE, "r") as file_h:
                data = json.load(file_h)
                self._validate_data(data)
                self._init_requirements(data["requirements"])
        except FileNotFoundError:
            pass

    def _init_requirements(self, req_data: list):
        self._req_data = req_data

    def _init_settings(self, settings_data: dict):
        self._next_id = settings_data["next_id"]

    def _safe_data(self):
        with open(REQUIREMENTS_FILE, "w") as file_h:
            out_data = self._get_save_data()
            self._validate_data(out_data)
            json.dump(out_data, file_h, indent=2, separators=(',', ': '))

    @staticmethod
    def _get_empty_requirement():
        return {"id": 0,
                "title": "",
                "description": None,
                "userstories": [],
                "owner": None,
                "status": True}

    def _id_exists(self, req_id: int) -> bool:
        for req in self._req_data:
            if req["id"] == req_id:
                return True
        return False

    def add_requirement(self, title: str, description: Optional[str], userstories: list, owner: Optional[str]):
        req = self._get_empty_requirement()
        req["title"] = title
        req["description"] = description
        req["userstories"] = userstories
        req["owner"] = owner
        req["id"] = self._next_id

        self._next_id += 1
        self._req_data.append(req)

    def get_requirements(self, valid: Optional[bool] = None) -> list[dict]:
        if valid is None:
            return self._req_data

        out_data = [x for x in self._req_data if x["valid"] is valid]
        return out_data
