# import all dependencies
import unittest
import json
from flaskr import create_app
from models import *
import os

database_name = "trivia_test"

class TriviaTestCase(unittest.TestCase):
    """This class represents the resource test case"""

    #Initialize datebase for testing
    def initializeDatabase():
        #delete existing test database
        bashCommand = "dropdb {}".format(database_name)
        os.system(bashCommand)
        #setup new test database
        bashCommand = "createdb {}".format(database_name)
        os.system(bashCommand)
        #load test database with example data
        bashCommand = "psql {} < {}.psql".format(database_name, database_name)
        os.system(bashCommand)

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = database_name
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres','localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass

    def request_invalid_questions_page(self):
        """ Test error for requesting invalid questions page """
        res = self.client().get('/question')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    # Test warning message if no categories are maintained in DB
    # def test_404_no_categories(self):
    #     """ Test abort for no categories """
    #     res = self.client().get('/categories')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'resource not found')

    def test_get_categories(self):
        """Test Categories display """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])



    def test_get_questions(self):
        """Test Categories display """
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_invalid_questions_page(self):
        """Test Categories display """
        res = self.client().get('/questions/page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        """ Create an endpoint to DELETE question using a question ID """
        res = self.client().delete('/questions/20')
        data = json.loads(res.data)
        #deleted_question = Question.query.filter(question.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 20)
        self.assertEqual(data['deleted_question'], None)

    def add_question(self):
        """ Create an endpoint to POST a new question """
        res = self.client().post('/questions/')
        # , json={'question': 'new question', 'answer': 'new_answer', 'catagory': "1", "difficulty": "3"}
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['question'], 'new question')
        self.assertEqual(data['answer'], 'new answer')
        self.assertEqual(data['category'], '1')
        self.assertEqual(data['difficulty'], '3')

'''
@TODO:

    def (self):
        """ Create a POST endpoint to get questions based on a search term. """

#   It should return any questions for whom the search term 
#   is a substring of the question. 

#   TEST: Search by any phrase. The questions list will update to include 
#   only question that include that string within their question. 
#   Try using the word "title" to start. 


    def (self):
        """ Create a GET endpoint to get questions based on category. """

    def (self):
                """ Create a POST endpoint to get questions to play the quiz """
#   Create a POST endpoint to get questions to play the quiz. 
#   This endpoint should take category and previous question parameters 
#   and return a random questions within the given category, 
#   if provided, and that is not one of the previous questions. 

#   TEST: In the "Play" tab, after a user selects "All" or a category,
#   one question at a time is displayed, the user is allowed to answer
#   and shown whether they were correct or not. 


Add test for no more new questions for current category => curl -X POST -H "Content-Type: application/json" -d '{"quiz_category":5, "previous_questions":[4, 6, 2]}' http://127.0.0.1:5000/quizzes

    def (self):
        """  """


  '''

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
