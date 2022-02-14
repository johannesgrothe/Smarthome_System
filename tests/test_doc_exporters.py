from export import export_api_docs, export_gadget_docs


def test_gadget_doc_export(temp_exists):
    export_gadget_docs()


def test_api_doc_export(temp_exists):
    export_api_docs()
