Semantic Textual Similarity :
Part A
1) load the data 
2) preprocess the textual data
3) Use CountVectorizer or TfIdf to convert text data into vectors 
4) find out the cosine similarity between texts 
5) similarity lies between 0 to 1. where 0 represents two sentences are not similar and 1 represents highly similar

Part B
deployment of model on heroku
1) create app.py file which will contain CountVectorizer method to get textual similarity. Streamlit an open source app framework in Python language is used.
2) requirement file for the required library that need to install on cloud server
3) other files required for model to build on heroku.


app link = https://heytext.herokuapp.com/
