.PHONY: gen

gen: genproto genopenapi


.PHONY: genproto

genproto:
	@echo "Gen Proto"
	@./scripts/genproto.sh
	@echo "Gen Proto Done"

.PHONY: genopenapi

genopenapi:
	@echo "Gen OpenAPI"
	@./scripts/genopenapi.sh
	@echo "Gen OpenAPI Done"

