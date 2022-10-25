import os
import subprocess
import base64
import stat
from typing import Tuple

banner = '''
                 __            __      __ 
    ____  ____  / /_  ______ _/ /___  / /_
   / __ \/ __ \/ / / / / __ `/ / __ \/ __/
  / /_/ / /_/ / / /_/ / /_/ / / /_/ / /_  
 / .___/\____/_/\__, /\__, /_/\____/\__/  
/_/            /____//____/               
'''

description = '''
============================================================
Hello Dear Hackers,

I really appreciate your program expliting skills, but, have
you ever heared of polyglot programming?

Yes or not, anyhow, this time, to win the flag, you just
need to submit a source code which fulfills the below 
requirements

  (1). Can be executed by the python3 interpreter
       without errors.
  (2). Can be compiled to executable ELF by the g++ 
       compilier, and can then be executed without
       errors.
  (3). The execution of (1) and (2) should output the
       same content in stdout
       
Moreover, the flag file, which is the target of your program,
is placed at /flag.txt.

Enjoy it.
============================================================
'''


def run_python_get_output(code: str) -> Tuple[str, int]:
    # 1. dump code to file
    py_filepath = "/tmp/polyglot.py"
    with open(py_filepath, "w") as f:
        f.write(code)
        f.flush()
        os.fsync(f.fileno())
    # 2. run it with python interpreter
    try:
        output = subprocess.check_output(["python3", py_filepath],
                                         stderr=open(os.devnull,
                                                     "w")).decode().strip()
        # 3. delete file and return
        os.unlink(py_filepath)
        return output, 0
    except Exception as _:
        return "", -1


def run_cpp_get_output(code: str) -> Tuple[str, int]:
    # 1. dump code to file
    cpp_filepath = "/tmp/polyglot.cpp"
    cpp_executablepath = "/tmp/polyglot.out"
    with open(cpp_filepath, "w") as f:
        f.write(code)
        f.flush()
        os.fsync(f.fileno())

    # 2. compile it with g++ compiler
    status = os.system(
        "g++ /tmp/polyglot.cpp -o {}".format(cpp_executablepath))
    if status:
        # os.unlink(cpp_filepath)
        return "", -1

    # 3. make sure executable flag
    st = os.stat(cpp_executablepath)
    os.chmod(cpp_executablepath, st.st_mode | stat.S_IEXEC)

    # 3. run it and get output
    try:
        output = subprocess.check_output([cpp_executablepath],
                                         stderr=open(os.devnull,
                                                     "w")).decode().strip()
        # 3. delete file and return
        # os.unlink(cpp_filepath)
        os.unlink(cpp_executablepath)
        return output, 0
    except Exception as _:
        return "", -1


def main() -> None:
    # 1. output banner
    print(banner, flush=True)
    # 2. output description
    print(description, flush=True)
    # 3. get the source code
    source_code_b64 = input("Give me your souce code (in base64 encode): ")
    try:
        source_code = base64.b64decode(source_code_b64).decode().strip()
        # 4. run this source code with python3
        py_output, status = run_python_get_output(source_code)
        if status:
            raise NameError("python run error")
        # 5. compile and run this source code with g++
        cpp_output, status = run_cpp_get_output(source_code)
        if status:
            raise NameError("cpp run error")
        # 6. final comparison
        if py_output == cpp_output:
            print("You are an awesome polyglot programmer~", flush=True)
            print(py_output, flush=True)
            return
        else:
            raise NameError("not equal run error")

    except Exception as err:
        print(err, flush=True)
        print("bad input", flush=True)
        return


if __name__ == '__main__':
    main()
