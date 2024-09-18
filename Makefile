.PHONY: run

run:
	@echo "Starting Django development server..."
	@python manage.py runserver

migrate:
	@echo "Migrating database..."
	@python manage.py makemigrations
	@python manage.py migrate