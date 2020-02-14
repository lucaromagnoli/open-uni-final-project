.PHONY: manage migrate migrations djangoshell

manage:
	docker-compose exec web python manage.py ${args}

migrate:
	docker-compose exec web python manage.py migrate ${args}

migrations:
	docker-compose exec web python manage.py makemigrations ${args}

djangoshell:
	docker-compose exec web python manage.py shell