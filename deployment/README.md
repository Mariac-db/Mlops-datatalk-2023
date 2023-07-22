## Deployment a model as a web-service

* Creating a virtual env with virtualenv (tengo windows humildemente)
pip install virtualenv
pip install --upgrade pip
cd my_project
virtualenv -p C:\Users\User\AppData\Local\Programs\Python\Python38\python.exe env
env\Scripts\activate

* Creating a script for predicting
* Putting the script into a Flask app
* Packing the app to docker


'''bash
docker build -t ride-duration-prediction-service:v1 .
'''

'''bash
docker run -it --rm -p 9696:9696  ride-duration-prediction-service:v1
'''

