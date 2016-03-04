all:
	@echo "If installation fails, use sudo or virtualenv"
	@echo
	pip install -r requirements.txt
	@echo
	@echo "Now, run 'make start' or simply 'python server.py'"
	@echo "If you want to publish to Kinesis, set up your Boto settings,"
	@echo "See https://github.com/boto/boto#getting-started-with-boto"

start:
	python server.py

test:
	curl -X POST -d"$$(date +%s)" http://localhost:8080/
