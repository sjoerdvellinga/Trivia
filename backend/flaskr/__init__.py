import os
from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# create and configure the app
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allowcd .. '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        # retrieve all categories from database
        categories = Category.query.order_by(db.desc(Category.id)).all()

        # error message if no categories are stored in/returned from database
        if len(categories) == 0:
            abort(404)

        return jsonify({
            'categories': {category.id: category.type
                           for category
                           in categories},
            'success': True,
            'total_categories': len(Category.query.all())
        })

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination
    at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    def paginate(request, quest_selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        current_questions = quest_selection[start:end]

        return current_questions

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        # retrieve all questions from database
        quest_selection = [question.format()
                           for question
                           in Question.query.all()]
        # limit max number of questions published per page
        current_questions = paginate(request, quest_selection)

        # retrieve all categories from database
        all_categories = Category.query.order_by(db.desc(Category.id)).all()

        # error message if no questions are stored in/returned from database
        if len(current_questions) == 0:
            abort(404)

        # API response in JSON format
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': {category.id: category.type
                           for category
                           in all_categories},
            'current_category': None,
        })
    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        # requested question
        question_data_query = Question.query.get(question_id)
        if question_data_query:
            Question.delete(question_data_query)
            result = {
                "success": True,
            }
            return jsonify(result)
        abort(404)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end
    of the last page of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        # capture data send by POST request
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        search_term = body.get('searchTerm', None)

        try:
            '''
            When search_term is provided the API shall return questions
            based on term.
            '''
            if search_term:
                search_results = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')).all()
                all_categories = Category.query.order_by(
                    db.desc(Category.id)).all()

                return jsonify({
                    'success': True,
                    'questions': [question.format()
                                  for question
                                  in search_results],
                    'total_questions': len(search_results),
                    'categories': {category.id: category.type
                                   for category
                                   in all_categories},
                    'current_category': None
                })

            # raise error when no data is provided in POST request
            if not ('question' in body and
                    'answer' in body and
                    'difficulty' in body and
                    'category' in body):
                abort(422)

            # else, add new question to database
            else:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty
                )
                question.insert()

                # API response in JSON format
                return jsonify({
                    'success': True,
                    'created': question.id,
                })
        except:
            abort(422)
    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_for_catagory(category_id):
        # retrieve questions for requested category from database
        quest_selection = [question.format()
                           for question
                           in Question.query.filter(
            Question.category == str(category_id)).all()]
        current_questions = paginate(request, quest_selection)

        # retrieve all questions from database
        all_categories = Category.query.order_by(db.desc(Category.id)).all()

        # error message if no questions are stored in/returned from database
        if len(current_questions) == 0:
            abort(404)

        # API response in JSON format
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': {category.id: category.type
                           for category
                           in all_categories},
            'current_category': category_id
        })

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    '''
    TODO: end-point taken from QuizView.js file in front-end.
    Check if this is correct.
    '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():

        try:
            body = request.get_json()
            # since the frontend returns the quiz_category
            # as dict {"type":'click', 'id':1}
            if isinstance(body['quiz_category'], dict):
                category_type = body['quiz_category']['id']
            else:  # to suit the request sent using the CURL and test scripts
                category_type = body['quiz_category']

            previous_questions = body['previous_questions']

            # if the category is "0", return all the questions
            if category_type == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            # else return questions within the selected category.
            elif category_type:
                questions = Question.query.filter(
                    Question.category == category_type,
                    Question.id.notin_(previous_questions)).all()

            # if the category is not available
            if len(questions) == 0:
                question = Question("", "", None, None).format()
            # else return random question from available questions
            # for catagory, excluding previous questions
            else:
                question = random.choice(questions).format()
            if question:
                return jsonify({
                    "success": True,
                    "question": question
                })
        except Exception:
            abort(404)

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "data is unprocessable"
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed for endpoint"
        }), 405

    return app
