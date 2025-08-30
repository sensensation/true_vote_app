# Running
start:
	docker-compose up --build -d

stop:
	docker-compose down

# Linting
flake8:
	docker-compose up -d app && docker exec -it carts flake8 .

imports:
	docker-compose up -d app && docker exec -it carts lint-imports

lint: flake8 imports

# Testing
test:
	docker-compose up -d app && \
	docker exec -it carts \
	pytest $(or $(target), tests) -p no:warnings -vv \
		   $(or $(foreach var, $(ignore), --ignore=$(var)), --ignore=tests/legacy) \
		   --cov=app --cov-report=term-missing

check: format lint test