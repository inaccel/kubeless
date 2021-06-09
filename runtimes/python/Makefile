all: build push

build:
	docker build --no-cache --tag inaccel/kubeless:python3.7 .

push:
	docker push inaccel/kubeless:python3.7
