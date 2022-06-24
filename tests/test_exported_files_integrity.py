def test_python_file_integrity():
    print("Importing python files to check integrity")
    import api_definitions
    import gadget_definitions
    print(api_definitions.api_version)
    print(api_definitions.ApiAccessLevel.admin)
    print(api_definitions.ApiURIs.test_echo)
    print(api_definitions.ApiEndpointCategory.System)


def test_cpp_file_integrity(assert_temp: str):
    print("Compiling c++ files to check integrity")
    import os
    return_code = os.system("g++ -o temp/test tests/cpp_compile_test.cpp -std=c++11")
    assert return_code == 0
    print("Executing c++ files to check included tests")
    return_code = os.system("./temp/test")
    assert return_code == 0


def test_js_file_integrity(assert_temp: str):
    print("Compiling js files to check integrity")
    import os
    os.system("ls")
    return_code = os.system(f"node --check api_definitions.js")
    print(return_code)
    # assert return_code == 0
    return_code = os.system(f"node --check gadget_definitions.js")
    # assert return_code == 0
    print(return_code)
