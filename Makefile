.PHONY: manage migrate migrations djangoshell flush taxonomy

manage:
	docker-compose exec web python manage.py ${args}

migrate:
	docker-compose exec web python manage.py migrate ${args}

migrations:
	docker-compose exec web python manage.py makemigrations ${args}

djangoshell:
	docker-compose exec web python manage.py shell

flush:
	docker-compose exec web python manage.py flush

taxonomy:
	docker-compose exec web python manage.py populate_taxonomy --file="/code/products/management/commands/taxonomy.csv"

server:
	docker-compose up; docker-compose up -d; docker-compose exec web python manage.py runserver ${args}

populate:
	docker-compose exec web python manage.py populate_raw_products --file=${file} --category=${category} --manufacturer=${manufacturer}