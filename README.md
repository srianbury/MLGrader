#MLGrader

This project was created to replace the traditional scantron used in schools in the US (I'm not sure if they're used else where).

#How to Use
TODO

##Motivation
Filling in bubbles and boxes on Scantrons is a hassel and takes too much time.  Students should be focused on reading and answering questions when taking an assessment, and not how well their bubbles are filled in.  Machine learning is as powerful as it has ever been and has an great solution for this problem.  Additionally, with this solution anyone with a copy of the document (available for free!) and a printer can print a test sheet.

##How it works
In this solution I have created an API that accepts an image and returns the answers as a json object.  I went with this approach because it allows my solution to be easily integrated with other educational systems such as blackboard.


##New Features
Here is a list of things I will try to add and want to implement.
1. Class Test Files
  - I have some files that I have written that allow you to test a specific function to see if its working.

2. Storage
  - Another advantage of this solution is the collection of data.  I have a small integration for MySQL but I would like to create storage in Google Cloud Platform or likewise.  This data would be used to improve the models as well as be available to the public for any other machine learning projects.
  
3. Model Code
  - The saved models are available but I need to add the Python Notebooks that created those models.
