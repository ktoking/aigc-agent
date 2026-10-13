PYTHON ?= python3
CONTROL = $(PYTHON) scripts/control.py

.PHONY: setup setup-mcp dev stop status doctor test research plan generate demo review publish-approved report install-service uninstall-service

setup:
	$(CONTROL) setup
setup-mcp:
	$(PYTHON) scripts/setup_mcp.py
dev:
	$(CONTROL) start $(ARGS)
stop:
	$(CONTROL) stop $(ARGS)
status doctor:
	$(CONTROL) doctor
test:
	$(CONTROL) test
research:
	$(CONTROL) research $(ARGS)
plan:
	$(CONTROL) plan $(ARGS)
generate:
	$(CONTROL) generate $(ARGS)
demo:
	$(CONTROL) demo
review:
	$(CONTROL) review $(ARGS)
publish-approved:
	$(CONTROL) publish-approved $(ARGS)
report:
	$(CONTROL) report
install-service:
	$(CONTROL) install-service
uninstall-service:
	$(CONTROL) uninstall-service
