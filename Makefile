install:
	poetry install

run: install
	poetry run python src/app.py

clean:
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} +