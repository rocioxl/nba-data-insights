run-server:
	export FLASK_APP=src/server/server.py;\
	flask run

drop-db:
	docker rm -f mysql_db_db_1;\
	docker volume rm mysql_db_my-db

start-db:
	docker-compose --file src/mysql_db/docker-compose.yml up  --build