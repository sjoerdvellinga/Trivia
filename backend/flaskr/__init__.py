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
        categories = Category.query.order_by(db.desc(Category.id)).all()

        if len(categories) == 0:
            abort(404)

        return jsonify({
        'categories': {category.id: category.type for category in categories},
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
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    def paginate(request, quest_selection):
        page = request.args.get('page', 1, type=int)
        start = (page -1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        current_questions = quest_selection[start:end]

        return current_questions

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        quest_selection = [question.format() for question in Question.query.all()]
        current_questions = paginate(request, quest_selection)

        all_categories = Category.query.order_by(db.desc(Category.id)).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(Question.query.all()),
        'categories': {category.id: category.type for category in all_categories},
        'current_category': None,
        })
    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            
            # if len(question) == 0:
            #   abort(404)
            
            question.delete()
            
            return jsonify({
                'success': True,
                'deleted': question_id,
            })
        
        except:
            abort(422)
    
    '''
    @TODO:
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        search_term = body.get('searchTerm', None)
    
        try:
            if search_term:
                search_results = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
                all_categories = Category.query.order_by(db.desc(Category.id)).all()

                return jsonify({
                'success': True,
                'questions': [question.format() for question in search_results],
                'total_questions': len(search_results),
                'categories': {category.id: category.type for category in all_categories},
                'current_category': None
                })

            if not ('question' in body 
                    and 'answer' in body 
                    and 'difficulty' in body 
                    and 'category' in body):
                abort(422)
                
            else:  
                question = Question(
                question=new_question, 
                answer=new_answer,
                category=new_category, 
                difficulty=new_difficulty)
                question.insert()

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
        quest_selection = [question.format() for question in Question.query.filter(
        Question.category == str(category_id)).all()]
        current_questions = paginate(request, quest_selection)
        all_categories = Category.query.order_by(db.desc(Category.id)).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': {category.id: category.type for category in all_categories},
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
    @app.route('/quizzes', methods=['POST'])
    # TODO: end-point taken from QuizView.js file in front-end. check if this is correct
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get("previous_questions")
        quiz_category = body.get("quiz_category")

        all_categories = Category.query.order_by(db.desc(Category.id)).all()

        if quiz_category:
            if not Category.query.get(quiz_category):
                abort(404)
            quiz_questions = Question.query.filter(
                Question.category.ilike(f'%{quiz_category}%'),
                Question.id.notin_(previous_questions)
            ).all()
        else:
            quiz_questions = Question.query.filter(
                Question.id.notin_(previous_questions)).all()

        if len(quiz_questions) == 0:
            return jsonify(None)
        else:
            questions = list(map(Question.format, quiz_questions))
            next_question = random.choice(questions)
            return jsonify({
                'success': True,
                'question': next_question,
                'quizCategory': next_question.catagory,
                'previousQuestions': previous_questions, 
                'categories': {category.id: category.type for category in all_categories},
                'currentQuestion': next_question
            })

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
        "message":"resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        "success": False,
        "error": 400,
        "message":"bad request"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message":"data is unprocessable"
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
        "success": False,
        "error": 405,
        "message":"method not allowed"
        }), 405

    return app

        