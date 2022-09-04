.DEFAULT_GOAL := prepare

prepare: install create-table

create-table:
	python3 create_table.py

install:
	pip install -r requirements.txt
