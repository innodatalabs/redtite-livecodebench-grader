import os
from aiohttp import web
from lcb_runner.evaluation import testing_util
import json


# LiveCodeBench plays dirty with os.environ and os.putenv, and trips on its own heels.
# disable this misguided attempt to create a secure sandbox.
def noop(*av, **kaw):
    pass
testing_util.reliability_guard = noop

async def ping_service(request):
    return web.json_response({ "status": "ok" })

async def run_test_service(request):
    testtype = request.match_info["testtype"]
    data = await request.json()

    code = data["code"]
    input_ = data["input"]
    output_ = data["output"]
    fn_name = data.get('name')
    timeout = data.get('timeout', 5)

    results, meta = testing_util.run_test({
            'input_output': json.dumps({
                'inputs': [input_],
                "outputs": [output_],
                "fn_name": fn_name,
            })
        },
        code,
        timeout=timeout
    )

    assert len(results) == 1

    return web.json_response({
        "success": results[0],
        "detail": meta
    })


app = web.Application()
app.router.add_get('/ping', ping_service)
app.router.add_post('/ping', ping_service)
app.router.add_post('/run_test/{testtype}', run_test_service)


if __name__ == "__main__":
    web.run_app(app, port=8000)