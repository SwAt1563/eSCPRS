
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


install i:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
	  echo "Usage: make $@ <library_name>"; \
	  exit 1; \
	fi

#	put / at the end of each line here imporant to save the library version varaible and use it with other commands

	@for lib_name in $(filter-out $@,$(MAKECMDGOALS)); do \
	  pip install $$lib_name; \
	  LIB_VERSION=$$(pip show $$lib_name | grep Version | awk '{print $$2}'); \
	  if [ -z "$$LIB_VERSION" ]; then \
	    echo "Failed to install $$lib_name"; \
	    exit 1; \
	  fi; \
	  echo "$$lib_name==$$LIB_VERSION" >> requirements.txt; \
	  echo "$$lib_name added to requirements.txt"; \
	done