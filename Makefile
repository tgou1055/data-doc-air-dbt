get-data:
	rm -rf ./data && rm -rf data.zip* && wget https://start-data-engg.s3.amazonaws.com/data.zip && unzip -o data.zip && chmod -R u=rwx,g=rwx,o=rwx data && rm -rf data.zip*

docker-spin-up:
	docker compose  --env-file env up airflow-init && docker compose --env-file env up --build -d

perms:
	sudo chmod -R u=rwx,g=rwx,o=rwx logs plugins temp dags dbt
