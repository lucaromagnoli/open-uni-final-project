migrate:
	docker-compose exec web python manage.py migrate ${args}

makemigrations:
	docker-compose exec web python manage.py makemigrations ${args}

shell:
	docker-compose exec web python manage.py shell