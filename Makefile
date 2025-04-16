build_run:
	docker build -t service . && docker run --rm -it --name service service
run:
	docker run --rm -it --name service service
test:
	docker exec -it service pytest -vvx tests/
