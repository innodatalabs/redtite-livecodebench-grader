TAG = ilabs/redlite-livecodebench-grader:latest

.PHONY: all docker push

all: docker

docker:
	docker build . -t $(TAG)
	echo 'Docker built!'

push:
	docker push $(TAG)
	echo 'Docker pushed!'