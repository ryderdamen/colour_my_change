IMAGE_NAME=gcr.io/radical-sloth/colour-my-change
VERSION=1.0.4
PWD = $(shell pwd)

.PHONY: build
build:
	@docker build -t $(IMAGE_NAME):$(VERSION) .

.PHONY: run
run:
	@echo "Running on http://0.0.0.0:5000/"; \
	docker run -p 5000:5000 -v $(PWD)/src/:/code/ $(IMAGE_NAME):$(VERSION)

.PHONY: push
push:
	@docker push $(IMAGE_NAME):$(VERSION)

.PHONY: deploy
deploy:
	@kubectl apply -f kubernetes/deployment.yaml -f kubernetes/service.yaml -f kubernetes/hpa.yaml
