# redlite-livecodebench-grader

A docker-based HTTP server that grades LiveCodeBench code generation tasks.

## Building

```bash
make docker
```

## Running

```bash
docker run -it -p 8000:80 ilabs/redlite-livecodebench-grader:latest
```

Server will me listening on local port 8000.

## API endpoints

### /ping

Useful to check server health

```http
GET /ping

{ "status": "ok" }
```

### /run_test/{testtype}

POST request that expects `application/json` body.

Here `testtype` can be either `stdin` or `functional`, depending on the task. Note that `functional` one requires passing
function name as a `name` field in the JSON payload.

JSON body should be structured as such:

* `code: str`: Python code to test
* `input: str`: test input. Could be several lines that is interpreted as several test inputs
* `output: str`: expected test output. If several lines of input were given, output should have the same number of lines
* `name: str | None`: name of the class function to call. If not given, tester assumes that code reads input from `stdin`
    and outputs answer to the `stdout`
* `timeout: int = 5`: number of seconds to wait for the code to complete (default is 5 sec)

Response will have the following structure:

* `success: bool`: True or False, depending on how test completed
* `meta: dict`: extra information pertaining to the test run (timing, and detail in case of a failed test)

