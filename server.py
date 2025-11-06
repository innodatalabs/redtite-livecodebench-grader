import os
from aiohttp import web
from runner import runner_stdin, runner_functional
import json
import ast


async def ping_service(request):
    return web.json_response({ "status": "ok" })


async def run_test_service(request):
    testtype = request.match_info["testtype"]
    data = await request.json()

    code = data["code"]
    inputs = data["inputs"]
    outputs = data["outputs"]
    name = data.get('name')
    timeout = data.get('timeout', 5)

    if testtype == 'stdin':
        out = runner_stdin(code, inputs, timeout=5)
    elif testtype == 'functional':
        out = runner_functional(code, name, inputs, timeout=timeout)
    else:
        raise RuntimeError(f"Unknown test type: {testtype}")

    success = len(out) == len(outputs) and all(_equals(x, y) for x,y in zip(outputs, out))

    return web.json_response({
        "success": success,
        "detail": {
            "expected": outputs,
            "actual": out,
        }
    })


def _equals(expected: str, actual: str) -> bool:
    # Expected string is in most cases result of json.dumps
    # Actual string is in most cases the result of repr or str of the returned value
    # Here we try to intelligently compare them
    expected = expected.strip()
    actual = actual.strip()
    if expected == actual:
        return True
    if actual.replace('True', 'true').replace('False', 'false') == expected:
        return True

    try:
        expected_json = json.loads(expected)
        actual_literal = ast.literal_eval(actual)
        if expected_json == actual_literal:
            return True
        if type(expected_json) is float and type(actual_literal) is float and abs(expected_json - actual_literal) < 1e-6:
            return True
    except:
        pass

    try:
        expected_json = json.loads(expected)
        if expected_json == actual:
            return True

        if json.loads(expected_json) == actual:
            return True
    except:
        pass

    return False

app = web.Application()
app.router.add_get('/ping', ping_service)
app.router.add_post('/ping', ping_service)
app.router.add_post('/run_test/{testtype}', run_test_service)


if __name__ == "__main__":
    web.run_app(app, port=8000)