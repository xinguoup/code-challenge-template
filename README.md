# Code Challenge Template

### Introduction
This is a solution of coding exercise, including ingesting some weather and crop yield data (provided), designing a database schema for it, and exposing the data through a REST API.

+ The folder of answers includes UML_graph, which is conceptual logical database design.
+ The folder of src includes all original code for problem 1, 2, 3, 4

### Run App
use `python src/problem4/app.py` to start the server.

### Run Test Case
- require Python >= 3.7
- use `pip install -r src/problem4/requirements.txt` to setup your ENV
- use `python src/problem4/app.py` to start the server.

### Extra Credit - Deployment
We could mainly use Docker to build an image, including building a python runtime environment based on requirements file and Copy the code and database to the mirror. Then we can upload the mirror we created to the mirror warehouse on AWS, and use the EC2 service of AWS to select the image we built to start a virtual machine on AWS. At this time, our service will also start. 