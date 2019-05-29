IMAGE_NAME=gcr.io/radical-sloth/lose-it-bubbles
VERSION=1.0.0
PWD = $(shell pwd)

.PHONY: build
build:
	@docker build -t $(IMAGE_NAME):$(VERSION) .

.PHONY: run
run:
	@echo "Running on http://0.0.0.0:5000/"; \
	docker run -p 5000:5000 -v $(PWD)/src/:/code/ $(IMAGE_NAME):$(VERSION)

.PHONY: push
	@docker push $(IMAGE_NAME):$(VERSION)
