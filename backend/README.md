# API Reference

## Getting Started
Base URL: *http://127.0.0.1:5000/*
Authentication: No authentication required.

## Error Handling
Errors are returned as JSON objects:

**Example**:
$ curl http://127.0.0.1:5000/NotValid

{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}

Other returned error codes:

400: Bad request
404: Resource not found
405: Method not allowed
422: Unprocessable

## Endpoints
### /categories    (method: GET)
*retrieve all categories*

**General**:
Returns lists of categories, success value and total number of categories.

**Example**:
$ curl http://127.0.0.1:5000/categories

{
  "categories": {
    "0": "Test", 
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 7
}


### /questions    (method: GET)
*retrieve all questions*

**General**:
Returns lists of categories, a list of questions, a success value and the total number of questions.
Results are paginated in groups (default per 10), include a request argument to choose page number, starting from 1 (which is also a default value)

**Example**:
$ curl http://127.0.0.1:5000/questions

{
  "categories": {
    "0": "Test", 
    "1": "Science", 
    < … >
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the 		Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      < … >
    }
  ], 
  "success": true, 
  "total_questions": 19
}

### /questions    (method: POST)
*add new question to the quiz*

**General**:
Creates a new question including the answer, the difficulty (value between 1 and 5) and category the question belongs to.

Returns success value, questions list paginated based on the page number, the inserted question, and total number of questions

**Example**:
$ curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"quesiton":"What is the nearest planet to the sun?", "answer":"Mercury", "difficulty":1, "category":1}'
{
    "success": True,
	“created”: 29
}

### /questions    (method: POST)
*search for questions based on search term*

**General**:
Returns success value, number of total questions,current category, and questions list that contains the given search term paginated baased on current page number.

**Example**:
$ curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'

    {
        "success":True,
        "questions":[
            {
                "question": " Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                "answer": "Maya Angelou",
                "category": "History",
                "difficulty": 2
            },
            {
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?
                "answer": "Edward Scissorhands",
                "category": "History",
                "difficulty": 3
            }
        ],
        "total_questions": 29
        "categories": {
    		  "0": "Test", 
    		  "1": "Science", 
    		  "2": "Art", 
    		  "3": "Geography", 
    		  "4": "History", 
    		  "5": "Entertainment", 
    		  "6": "Sports"
  }, 

         "current_category": None

    }
  }

### /categories/<int:category_id>/questions    (method: GET)
*retrieve all questions in a category*

**General**:
Get all the questions, paginated to 10 questions a page assigned to a specified category.
(10 is default max questions per page).

Returns the categories, current/selected category, list of questions belonging to the current category, success value and the total number of questions.

**Example**:
$ curl -X GET http://127.0.0.1:5000/categories/1/questions

{
  "categories": {
    "0": "Test", 
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}

### /questions    (method: DELETE)
*delete a specific question*

**General**:
Deleted the question with the given ID, if exists
Returns success value, the deleted question id, the number of total questions, and questions list paginated based on the current page number.

**Example**:
$ curl -X DELETE http://127.0.0.1:5000/questions/31

{
  "deleted": 31, 
  "questions": [
    {
      "answer": "ear", 
      "category": 1, 
      "difficulty": 3, 
      "id": 31, 
      "question": "On what part of your body would you find the pinna?"
    }, 
    {
      "answer": "Mercury", 
      "category": 1, 
      "difficulty": 1, 
      "id": 29, 
      "question": "What is the nearest planet to the sun?"
    }, 
    {
      < … >
    }, 
  ], 
  "success": true, 
  "total_questions": 20
}

### /quizzes    (method: GET)
*Get a new question*

**General**:
Returns a random next question respecting category and previous questions

Input: 
“quiz_category” (string) or (dict)
“previous_questions” (array) (optional)

Example:
$ curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"quiz_category":5, "previous_questions":[]}'

{
  "success": True,
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 2,
    "id": 22,
    "question": “Hematology is a branch of medicine involving the study of what?”
  }
}
