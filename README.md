### Test project for InStandart

#### git clone https://github.com/bandirom/Django-project-with-Faker.git

#### In root dir for dev for starting dev server
    docker-compose up -d --build
    
#### Prod version:
    docker-compose -f prod.yml up -d --build
    
#### Seem the logs dev:
    docker-compose logs -f
    
#### Seem the logs prod:
    docker-compose -f prod.yml logs -f
    
#### Local dev server: 
##### [http://localhost:8002](http://localhost:8002)

#### Prod server: 
##### [http://localhost](http://localhost)
## Important!!! You should create a superuser for working there
     docker-compose exec web python manage.py createsuperuser
#### or
    docker-compose -f prod.yml exec web python manage.py createsuperuser

## Description:
##### On the main page after authorization you will see 3 tabs: Users, Companies, Abusers
##### Click "Generate users" and reload page after few seconds. Celery processed task
##### Also will be generated companies from default list in web/app/services.py: companies 

You can create companies and users manual. Also edit/remove it.

##### In 'Abuses' tabs you can find 'Generate data' button. 
When you push it will create a Celery task and will be generating 180 days of data for each user
    
    web/app/services.py: DATE_RANGE
    
After reload the page you have a choice of different month. After click 'Show data' table will be completely full 



### Also important: Basic django templates and modules from my basic project
#### https://github.com/bandirom/django_with_docker