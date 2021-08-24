Netguru_Cars
============
 A rating webapp for cars that allows adding, deleting and rating cars to a database.

Requirements and setup
----------------------

    To setup the project make sure you first copy the project to your desired directory 
    and create a virtual environment using:
        :code:`>python -m venv` 
        `Venv documentation https://docs.python.org/3/library/venv.html>`_
    
    After activating your virtual environment, please install requirements:
        :code:`>pip install -r requirements.txt`
        
    To start the server use:
        :code:`>python manage.py runserver`
    
    Api will be available at:
        http://127.0.0.1:8000/
        
Endpoints
---------
    
    Below are relative links to base url: http://127.0.0.1:8000/ 
    - 'cars/'
        * GET - returns a json response with a list of all available cars in the database of the form:
                [{"id": 1, "make": "Audi", "model": "Q7", "avg_rating": 4.0}, 
                 {"id": 2, "make": "Volkswagen", "model": "Golf", "avg_rating": 4.5}]
        * POST - adds a car to the database. First checks if the car is available in external api, 
                 then if the car isn't already in internal database, creates the car in the database.
                 external api at: https://vpic.nhtsa.dot.gov/api/
                 Expects a json in the body of the request, of the form: {"make": "Audi", "model": "Q7"}
                 
    - 'cars/{id}/'
        * DELETE - deletes a car from the database, identifying it by provided id 
                   or returns error if id is not in the database.
                   
    - 'rate/'
        * POST - attributes a rating to a car that is in the database. If the car is not in the database, returns Error.
                 Expects a json in the body of the request, of the form: {"car_id" : 1, "rating" : 5}
                 
    - 'popular/'
        * GET - returns a json response with a list of all available cars in the database,
                sorted by number of ratings that each car received, in the form:
                [{"id": 2, "make": "Volkswagen", "model": "Golf", "rates_number"": 45},
                 {"id": 1, "make": "Audi", "model": "Q7", "rates_number": 40}]
