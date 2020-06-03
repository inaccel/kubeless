all: build-all push-all

build-all: build3.6 build3.7

push-all: push3.6 push3.7

build3.6:
	docker build --file Dockerfile.3.6 --no-cache --tag inaccel/kubeless:python3.6 .

build3.7:
	docker build --file Dockerfile.3.7 --no-cache --tag inaccel/kubeless:python3.7 .

push3.6:
	docker push inaccel/kubeless:python3.6

push3.7:
	docker push inaccel/kubeless:python3.7
