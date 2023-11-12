SHELL = /bin/sh

up:
	docker compose up --detach

up-build:
	docker compose up --build --detach

start:
	docker compose start

stop:
	docker compose stop

down:
	docker compose down

logs-watch:
	docker compose logs --follow

.PHONY: up up-build start stop down logs-watch
