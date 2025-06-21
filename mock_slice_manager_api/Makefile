init:
	python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt && deactivate

run:
	. venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload  && deactivate