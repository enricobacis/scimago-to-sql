.PHONY  : all clean run

VENV   = venv
MAIN   = scimagojr.py

all run: $(VENV)
	$(VENV)/bin/python $(MAIN)

clean:
	@ rm -rf $(VENV) build dist *.egg-info
	@ rm -rf *.pyc *.pyo __pycache__

$(VENV): requirements.txt
	virtualenv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
