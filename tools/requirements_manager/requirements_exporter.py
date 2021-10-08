class RequirementsExporter:

    @classmethod
    def _format_requirement(cls, req: dict) -> list[str]:
        out_data: list[str] = []
        owner = req['owner']
        if not owner:
            owner = "None"
        out_data.append(f"##{req['title']}")
        out_data.append(f"ID: {req['id']}")
        out_data.append(f"Owner: {owner}")
        status = "Valid" if req['status'] else "Deprecated"
        out_data.append(f"Status: {status}")

        out_data.append(f"###Description")
        out_data.append(req['description'])
        out_data.append(f"###Userstories")
        for story in req['userstories']:
            out_data.append(f"`{story}`")
        return out_data

    @classmethod
    def export_markdown(cls, requirements: list, filename: str):
        out_data: list[str] = ["#Requirements", ""]

        for req in requirements:
            req_data = cls._format_requirement(req)
            out_data += req_data
            out_data.append("")

        write_data = [f"{x}\n" for x in out_data if not x.endswith("\n")]

        with open(filename, "w") as file_h:
            file_h.writelines(write_data)
