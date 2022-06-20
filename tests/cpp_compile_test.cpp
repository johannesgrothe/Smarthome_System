#include "../api_definitions.h"
#include "../gadget_definitions.h"

#include <iostream>
#include <sstream>

int main() {
    std::stringstream test_stream;
    test_stream << api_definitions::uris::test_echo;
    test_stream << api_definitions::version::major;

    return 0;
}
