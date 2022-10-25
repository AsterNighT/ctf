export INCLUDE_PATH
CXXFLAGS = -I$(INCLUDE_PATH) -O2 --std=c++17

all: chk judger val

% : %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@
