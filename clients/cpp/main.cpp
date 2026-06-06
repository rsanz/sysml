#include <iostream>
#include <string>

int main(int argc, char** argv) {
  const std::string base = argc > 1 ? argv[1] : "http://127.0.0.1:9000";
  const std::string endpoint = argc > 2 ? argv[2] : "/about";
  std::cout << "curl -fsSL " << base << endpoint << std::endl;
  return 0;
}
