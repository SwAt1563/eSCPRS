
.PHONY: run config push pull install



run:
	@docker-compose -f ./docker-compose-mongodb.yml --env-file .env.dev up -d
	@docker-compose -f ./docker-compose-ollama.yml --env-file .env.dev up -d 
	@docker-compose -f ./docker-compose.yml --env-file .env.dev up 


# To avoid line ending conversion on windows
config:
	@git config core.autocrlf false


push:
	@git add . && \
	echo "Enter commit message:" && \
	read commit_message && \
	git commit -m "$$commit_message" && \
	git push


pull:
	@git pull
