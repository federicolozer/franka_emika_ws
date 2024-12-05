#include "global.hpp"
#include "nsga3.hpp"

int main() {

	size_t num_exp 	= 20;	// total number of experiments (runs)
	numVariables 	= 12; 	// number of variables (M+k-1) = (3+10-1), k=10
	strcpy(strTestInstance,"DTLZ2");

	ifstream indata("/home/lozer/franka_emika_ws/src/path_planning/src/TestDTLZ2.txt");
	if (!indata) {
		cerr << "Error: file could not be opened" << endl;
		exit(1);
	}

	char temp[1024];
	while(!indata.eof()) {
		indata >> temp >> numObjectives;
		indata >> temp >> max_gen;
		indata >> temp >> p_boundary;
		indata >> temp >> p_inside;

		for (size_t run = 1; run <= num_exp; ++run) {
			printf(" Running experiment %lu for %s problem with %d objectives\n",
					run, strTestInstance, numObjectives);

			seed = (seed + 111) % 1235;
			rnd_uni_init = -(long) seed;

			NSGA3 NSGA3_optimizer;
			NSGA3_optimizer.run(max_gen, run);
		}
	}
	indata.close();
	return 1;
}
