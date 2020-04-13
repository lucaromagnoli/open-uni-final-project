.PHONY: manage migrate migrations djangoshell flush taxonomy server populate heroku-populate

db:
	docker-compose run db

manage:
	docker-compose exec web python manage.py ${args}

migrate:
	docker-compose exec web python manage.py migrate ${args}

heroku-migrate:
	heroku run python manage.py migrate ${args}

migrations:
	docker-compose exec web python manage.py makemigrations ${args}

djangoshell:
	docker-compose exec web python manage.py shell

flush:
	docker-compose exec web python manage.py flush

taxonomy:
	docker-compose exec web python manage.py populate_taxonomy --file=${file}

heroku-taxonomy:
	heroku run python manage.py populate_taxonomy --file=${file}

server:
	docker-compose down; docker-compose up -d; docker-compose exec web python manage.py runserver ${args}

populate:
	docker-compose exec web python manage.py populate_products --file=${file} --category=${category} --manufacturer=${manufacturer}

heroku-populate:
	heroku run python manage.py populate_products --file=${file} --category=${category} --manufacturer=${manufacturer}

heroku-deploy:
	git push heroku master
