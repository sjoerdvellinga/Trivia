import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

database_name = "trivia_test"

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    # def initializeDatabase():
    #     """Build test database to execute test cases"""
    #     #delete existing test database
    #     bashCommand = "dropdb {}".format(database_name)
    #     os.system(bashCommand)
    #     #setup new test database
    #     bashCommand = "createdb {}".format(database_name)
    #     os.system(bashCommand)
    #     #load test database with example data
    #     bashCommand = "psql {} < {}.psql".format(database_name, database_name)
    #     os.system(bashCommand)

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = database_name
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        # input to submit a new question (positive test)
        self.add_question = {
            "question": "Whats is Caryn McCarthy's favorite author?",
            "answer": "Neill Gaiman",
            "difficulty": 1,
            "category": 2
        }
        # failure to submit a new question (negative test)
        self.fail_add_question = {
            # 'difficulty' is missing!
            "question": "What planet is closed to the sun?",
            "answer": "Mercury",
            "category": 1
        }

        #input for play game (positive test)
        self.play_quiz = {
            "quiz_category":5,
            "previous_questions":[5,]
        }
    
        #error for input to play game (negative test)
        self.error_play_quiz = {
            "quiz_category":"Entertainment",
            "previous_questions":[5,]
        }

        self.wrongdata_play_quiz = {
            "field01":"Something not existing",
            "field02":"Something else not existing"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        """ Test GET /categories """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])

    # Test warning message if no categories are maintained in DB
    # def test_404_no_categories(self):
    #     """ Test abort for no categories """
    #     res = self.client().get('/categories')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'resource not found')

    def test_get_category_id(self):
        """ Test not supported GET method /questions """
        response = self.client().get('/categories/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['success'], False)


    def test_get_questions(self):
        """ Test GET /questions """
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_get_question_id(self):
        """ Test not supported GET method /questions """
        response = self.client().get('/questions/5')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['message'], 'method not allowed for endpoint')
        self.assertEqual(data['success'], False)

    def test_get_paginated_questions(self):
        result = self.client().get('/questions?page=1')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["questions"]))

    def test_404_get_paginated_questions_beyond_valid_page(self):
        result = self.client().get('/questions?page=9999')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_add_question(self):
        """ Test adding new question to database """
        # count number of questions in initial db
        initial_questions = len(Question.query.all())
        # post new question to db
        response = self.client().post("/questions", json=self.add_question)
        data = json.loads(response.data)
        # count new number of questions in db
        new_questions = len(Question.query.all())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(new_questions - initial_questions == 1)

    def test_search_questions(self):
        """ return result for search term strings """
        response = self.client().post("/questions",
            json={"searchTerm": "title"})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["questions"]), 2)
    
    def test_delete_question(self):
        """ Test DELETE method for '/questions' using unique question ID """
        response = self.client().delete('/questions/20')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["total_questions"])

    def test_404_delete_question(self):
        result = self.client().delete('/questions/9999')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_invalid_questions_page(self):
        """Test GET invalid questions page """
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_category(self):
        """ Test GET questions for given category """
        response = self.client().get("/categories/2/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        
    def test_get_questions_category_error(self):
        """ Test GET questions for not existing category """
        response = self.client().get("/categories/99/questions")

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_add_question(self):
        """ Test POST new question """
        # count number of questions in initial db
        initial_questions = len(Question.query.all())
        # post new question to db
        response = self.client().post("/questions", json=self.add_question)
        data = json.loads(response.data)
        # count new number of questions in db
        new_questions = len(Question.query.all())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(new_questions - initial_questions == 1)

    def test_422_post_new_question(self):
        # post new question to db, with 1 missing field (difficulty)
        response = self.client().post("/questions", json=self.fail_add_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "data is unprocessable")

    def test_get_paginated_question_by_category(self):
        response = self.client().get('/categories/1/questions?page=1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["questions"]))

    def test_404_get_paginated_question_by_category_beyond_valid_page(self):
        response = self.client().get('/categories/1/questions?page=100')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_play_game(self):
        response = self.client().post("/quizzes", json=self.play_quiz)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_play_game(self):
        response = self.client().post("/quizzes", json=self.error_play_quiz)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_422_play_game(self):
        response = self.client().post('/quizzes', json=self.wrongdata_play_quiz)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()