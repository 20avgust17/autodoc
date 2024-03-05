1. Pull the main branch to the local repository.
2. Start Docker desktop.
3. In Pycharm terminal run the command "docker-compose -f docker-compose.local.yml up --build"
4. After building the containers, run command "docker-compose -f docker-compose.local.yml run src alembic upgrade head"
5. To view api use url - http://localhost:8088/docs#/
6. Run the command "docker-compose -f docker-compose.local.yml run src pytest -v" for view result of tests

additional special features you implemented.
1. Implemented dockerisation of the application
2. Implemented user authorisation with jwt, to work with game items you need to create an account and authorise first
3. Added category table for Game items (one-to-many)
4. Implemented basic operations for categories 
5. Added logging specifically for Game items service
6. Implemented extended documentation for swagger specifically for Game items
7. The .env file is in the repository 
