#include "testlib.h"

int main(int argc, char * argv[])
{
	registerTestlibCmd(argc, argv);

	int pa = ouf.readInt();
	if (pa == 1) {
		testlibMode = _interactor; // hack: allow more outputs
		quitf(_ok, "answer is ok");
	} else {
		quitf(_wa, "answer is not ok");
	}
}
