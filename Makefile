migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations ${arg}

shell:
	docker-compose exec web python manage.py shell