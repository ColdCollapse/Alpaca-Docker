#!make

# Importing environment variables
-include .env.dist
-include .env
-include .env.dev
-include .env.override
export

# Variables
DOCKER = docker
define DOCKER_COMPOSE
@if [ ! -f .env.merged ]; then \
  echo "ℹ️ .env.merged not found. Auto-generating..."; \
  $(MAKE) env-merge; \
fi; \
docker compose --env-file .env.merged
endef
EXEC = $(DOCKER) exec -it $(REDIS_CONTAINER_NAME)

# Colors
GREEN = /bin/echo -e "\x1b[32m\#\# $1\x1b[0m"
RED = /bin/echo -e "\x1b[31m\#\# $1\x1b[0m"

## —— 🔥 App ——————————————————————————————————————————————————————————————————
.PHONY: init
init: ## Init the project
	$(MAKE) env-merge
	$(MAKE) ensure-network
	$(MAKE) build
	$(MAKE) docker-start
	@$(call GREEN,"The application installed successfully.")

.PHONY: cli
cli: ## Opens the redis-cli
	$(DOCKER_COMPOSE) up -d redis-bus
	$(MAKE) redis-cli

.PHONY: sh
sh: ## Opens a shell in the redis container
	$(DOCKER_COMPOSE) up -d redis-bus
	$(MAKE) redis-sh

.PHONY: redis-sh
redis-sh:
	$(DOCKER_COMPOSE) exec -it redis-bus /bin/sh

.PHONY: redis-cli
redis-cli:
	$(DOCKER_COMPOSE) exec -it redis-bus redis-cli

## —— ✅ Test ——————————————————————————————————————————————————————————————————
.PHONY: test
test: ## Run all tests
	$(MAKE) test-smoke

.PHONY: test-smoke
test-smoke: ## Run smoke tests
	$(MAKE) ensure-network
	$(DOCKER_COMPOSE) up -d redis-bus
	bash tests/smoke.sh
	$(DOCKER_COMPOSE) stop

## —— 🐳 Docker ———————————————————————————————————————————————————————————————
.PHONY: build
build: ## Build app with fresh images
	$(DOCKER_COMPOSE) build

.PHONY: start
start: ## Start the app
	$(MAKE) docker-start

.PHONY: docker-start
docker-start:
	$(DOCKER_COMPOSE) up -d

.PHONY: stop
stop: ## Stop app
	$(MAKE) docker-stop

.PHONY: down
down: ## Stop app
	$(MAKE) docker-down

.PHONY: docker-stop
docker-stop:
	$(DOCKER_COMPOSE) stop
	@$(call GREEN,"The containers are now stopped.")

.PHONY: docker-down
docker-down:
	$(DOCKER_COMPOSE) down
	@$(call GREEN,"The containers are now down.")

.PHONY: terminate
terminate: ## Unsets all the set
	$(MAKE) stop
	$(DOCKER_COMPOSE) down --remove-orphans --volumes
	$(DOCKER_COMPOSE) rm -vsf
	@$(call GREEN,"The application was terminated successfully.")

.PHONY: rebuild
rebuild: ## Rebuilds all docker containers
	$(MAKE) terminate
	$(MAKE) init

.PHONY: env-merge
env-merge: ## Merges all .env files to override all variables to be able using local definitions
	@cat /dev/null \
		$(shell [ -f .env.dist ] && echo .env.dist) \
		$(shell [ -f .env ] && echo .env) \
		$(shell [ -f .env.dev ] && echo .env.dev) \
		$(shell [ -f .env.override ] && echo .env.override) \
		| grep -v '^#' | grep -v '^$$' | awk -F= '!seen[$$1]++' > .env.merged

.PHONY: ensure-network
ensure-network: ## Ensures that shared network exists and create it otherwise
	@docker network inspect $(REDIS_NETWORK) >/dev/null 2>&1 || (docker network create $(REDIS_NETWORK) && echo "✅ Created network: $(REDIS_NETWORK)")

## —— 🛠️ Others ——————————————————————————————————————————————————————————————

.PHONY: help
help: ## List of commands
	@grep -E '(^[a-zA-Z0-9_-]+:.*?##.*$$)|(^##)' Makefile | awk 'BEGIN {FS = ":.*?## "}{printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'
