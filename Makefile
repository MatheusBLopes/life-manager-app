PROJECT_NAME = $(shell pwd | rev | cut -f1 -d'/' - | rev)

runserver:
	poetry run python life-manager-app/manage.py runserver

migrate:
	poetry run python life-manager-app/manage.py migrate

makemigrations:
	poetry run python life-manager-app/manage.py makemigrations

lint:
	poetry run pre-commit run --all-files

run-gunicorn:
	gunicorn -c gunicorn_config.py quizhero_api.wsgi:application

test:
	poetry run pytest -sx $(PROJECT_NAME) --reuse-db --create-db

collect-static:
	poetry run python life-manager-app/manage.py collectstatic

createsuperuser:
	poetry run python life-manager-app/manage.py createsuperuser

seed:
	poetry run python life-manager-app/manage.py seed

clean-seed:
	poetry run python life-manager-app/manage.py seed --clean

# SSH
generate-prod-key:
	cd iac/ && ssh-keygen -t rsa -b 2048 -f quizhero-prod-key-pair.pem

generate-dev-key:
	cd iac/ && ssh-keygen -t rsa -b 2048 -f quizhero-dev-key-pair.pem

change-permission:
	chmod 400 ./iac/quizhero-key-pair.pem

dev-ssh:
	cd iac/ && ssh -i ./iac/quizhero-dev-key-pair.pem ec2-user@----ip------

prod-ssh:
	cd iac/ && ssh -i ./iac/quizhero-prod-key-pair.pem ec2-user@----ip------

# DOCKER
run-container:
	docker run -p 8000:8000 life-manager-app


# TERRAFORM

tf-dev-env:
	cd iac/ && terraform workspace select dev

tf-apply-dev:
	cd iac/ terraform apply -var-file=vars-dev.tfvars
	
tf-prod-env:
	cd iac/ && terraform workspace select prod

tf-apply-prod:
	cd iac/ terraform apply -var-file=vars-prod.tfvars

