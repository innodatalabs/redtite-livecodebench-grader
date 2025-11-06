import tempfile
import subprocess
import os


def runner_stdin(code: str, inputs: list[str], timeout: int = 5):
    with tempfile.TemporaryDirectory() as tmpdir:
        fname = os.path.join(tmpdir, "solution.py")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(code)

        results = [_run(fname, input_, timeout) for input_ in inputs]
        return results


_WRAPPER_CODE = """
from typing import List  # common error not importing List, should not fail

{code}
if __name__ == '__main__':
    import sys
    import json
    inputs = [json.loads(x) for x in sys.stdin.read().splitlines()]
    solution = Solution()
    print(solution.{function}(*inputs))
"""


def runner_functional(code: str, function, inputs: list[str], timeout: int = 5):
    with tempfile.TemporaryDirectory() as tmpdir:
        fname = os.path.join(tmpdir, "solution.py")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(_WRAPPER_CODE.format(code=code, function=function))

        results = [_run(fname, input_, timeout) for input_ in inputs]
        return results


def _run(fname: str, input_: str, timeout: int = 5):
        try:
            completed_process = subprocess.run(
                ["python3", fname],
                input=input_,
                text=True,
                capture_output=True,
                timeout=timeout,
            )
            if completed_process.returncode != 0:
                return f"ERROR: {completed_process.stderr.strip()}"
            return completed_process.stdout.strip()
        except BaseException as e:
            return f"ERROR: {str(e)}"
