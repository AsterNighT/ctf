#include "uoj_judger.h"
#include <fstream>
#include <cassert>
using namespace std;

string judge_key;

PointInfo my_test_point(int num) {
	string input = work_path + "/" + "convince.in";
	string plain_input = data_path + "/" + conf_file_name_with_num("input", num);
	string output = work_path + "/" + "convince.out";
	string plain_output = work_path + "/" + "convince.plain.out";

	file_encrypt(plain_input, input, judge_key);

	RunResult res = run_submission_program(
			input,
			output,
			conf_run_limit(num, RL_DEFAULT),
			"answer");

	bool auth = file_decrypt(output, plain_output, judge_key);
	if (res.type != runp::RS_AC) {
		PointInfo po(num, 0, -1, -1, info_str(res.type));
		po.li.push_back(InfoBlock::from_file("input", plain_input));
		// po.li.push_back(InfoBlock::from_file("output", plain_output));
		po.li.push_back(InfoBlock::from_string("res", info_str(res.type)));
		return po;
	}
	if (!auth) {
		PointInfo po(num, 0, res.ust, res.usm, info_str(res.type));
		po.li.push_back(InfoBlock::from_file("input", plain_input));
		// po.li.push_back(InfoBlock::from_file("output", plain_output));
		po.li.push_back(InfoBlock::from_string("res", "Unauthorized output"));
		return po;
	}
	
	file_hide_token(plain_output, conf_str("split_token", ""));

	RunCheckerResult chk_ret = run_checker(
			conf_run_limit("checker", num, RL_CHECKER_DEFAULT),
			data_path + "/chk",
			plain_input,
			plain_output,
			plain_output);
	if (chk_ret.type != runp::RS_AC) {
		PointInfo po(num, 0, -1, -1, "Checker " + info_str(chk_ret.type));
		po.li.push_back(InfoBlock::from_file("input", plain_input));
		po.li.push_back(InfoBlock::from_file("output", plain_output));
		po.li.push_back(InfoBlock::empty("res"));
		return po;
	}

	PointInfo po(num, chk_ret.scr, res.ust, res.usm);
	po.li.push_back(InfoBlock::from_file("input", plain_input));
	po.li.push_back(InfoBlock::from_file("output", plain_output));
	po.li.push_back(InfoBlock::from_string("res", chk_ret.info));
	return po;
}

void ordinary_test() {
	int n = conf_int("n_tests", 1);

	bool passed = true;
	for (int i = 1; i <= n; i++) {
		report_judge_status_f("Judging Test #%d", i);
		PointInfo po = my_test_point(i);
		if (po.scr != 100) {
			passed = false;
		}
		po.scr = scale_score(po.scr, conf_int("point_score", i, 100 / n));
		add_point_info(po);
	}

	if (!passed) {
		end_judge_ok();
	}

	tot_score = 100;
	end_judge_ok();
}

int main(int argc, char **argv) {
	judger_init(argc, argv);

	file_copy(main_path + "/include/uoj_secure.h", work_path + "/" + "uoj_secure.h");

	judge_key = gen_token();
	string impl = "implementer_" + gen_token();

	report_judge_status_f("Compiling");
	file_move(work_path + "/" + "implementer.cpp", work_path + "/" + impl + ".cpp");
	file_replace_tokens(work_path + "/" + impl + ".cpp", conf_str("token"), judge_key);
	RunCompilerResult c_ret = compile_with_implementer("answer", impl);
	if (!c_ret.succeeded) {
		end_judge_compile_error(c_ret);
	}

	assert(!conf_is("test_sample_only", "on"));

	ordinary_test();

	end_judge_ok();
}
