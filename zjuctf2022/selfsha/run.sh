g++ main.cpp
./a.out > main.cpp.sha256
sha256sum main.cpp | awk '{print $1}' > main.cpp.sha256.yes
diff main.cpp.sha256 main.cpp.sha256.yes