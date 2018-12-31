# MLGrader

This project was created to replace the traditional scantron used in schools in the US (I'm not sure if they're used else where).

# How to Use
(I am a windows user, any changes/additions for other users are greatly appreciated)
1. Clone Repo
  - git clone https://github.com/srianbury/MLGrader.git
2. Change to the new directory
  - cd MLGrader
3. Create a virtual environment named venv (or whatever you like)
  - virtualenv -p C:\Python36\python.exe venv 
  - (I used the full path to Python because I have 3.6 and 2.7 and everything goes crazy if I dont give the full path)
4. Start the virtual environment
  - venv\scripts\activate
5. Install dependencies
  - pip install -r requirements.txt
6. Start the server
  - python main.py (this will start the server and allow you to call the API)
7. Calling the API
  - I use Postman but any API development program will be fine
  - Request Type: POST
  - URL: http://127.0.0.1:5000/
  - Header: Key: Content-Type, Value: image/jpeg
  - Body: Key: image, value: brians_test.jpeg (or your test file)

## Motivation
Filling in bubbles and boxes on Scantrons is a hassel and takes too much time.  Students should be focused on reading and answering questions when taking an assessment, and not how well their bubbles are filled in.  Machine learning is as powerful as it has ever been and has an great solution for this problem.  Additionally, with this solution anyone with a copy of the document (available for free!) and a printer can print a test sheet.

## How it works
In this solution I have created an API that accepts an image and returns the answers as a json object.  I went with this approach because it allows my solution to be easily integrated with other educational systems such as blackboard.


## New Features
Here is a list of things I will try to add and want to implement.
1. Class Test Files
  - I have some files that I have written that allow you to test a specific function to see if its working.

2. Storage
  - Another advantage of this solution is the collection of data.  I have a small integration for MySQL but I would like to create storage in Google Cloud Platform or likewise.  This data would be used to improve the models as well as be available to the public for any other machine learning projects.
  
3. Model Code
  - The saved models are available but I need to add the Python Notebooks that created those models.
  
4. Simple React App
  - Create a simple react app where the api is consumed and results are displayed
