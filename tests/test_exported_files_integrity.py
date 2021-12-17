def test_python_file_integrity():
    print("Importing python files to check integrity")
    import api_definitions
    import gadget_definitions
    buffer = api_definitions.ApiURIs.test_echo
    buffer = gadget_definitions.GadgetIdentifier.any_gadget


def test_cpp_file_integrity(temp_exists):
    print("Compiling c++ files to check integrity")
    import os
    return_code = os.system("g++ -o temp/test tests/cpp_compile_test.cpp -std=c++11")
    assert return_code == 0
    print("Executing c++ files to check included tests")
    return_code = os.system("./temp/test")
    assert return_code == 0
