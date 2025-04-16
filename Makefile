run:
	docker build -t service . && docker run --rm -it --name service service

test:
	docker build -t service-test -f Dockerfile.test .
	docker run --rm -it --name service-test service-test
