
.PHONY: all docs tests

reformat:
	black -l 79 .
	isort -l79 --profile black .

tests:
	tox -r

requirements:
	pipenv requirements > requirements.txt
	pipenv requirements --dev > requirements-dev.txt

coverage:
	coverage report
	coverage html -i

build-dev:
	docker build -t repository-service-tuf-api:dev .

run-dev:
	$(MAKE) build-dev
	docker pull ghcr.io/vmware/repository-service-tuf-worker:dev
	docker-compose up --remove-orphans

stop:
	docker-compose down -v

clean:
	$(MAKE) stop
	docker-compose rm --force
	rm -rf ./metadata/*
	rm -rf ./keys/*
	rm -rf ./database/*.sqlite
	rm -rf ./data
	rm -rf ./data_test

purge:
	$(MAKE) clean
	docker rmi repository-service-tuf-api_repository-service-tuf-rest-api --force


docs:
	tox -e docs