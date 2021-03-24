import os

#Initialize datebase for testing
testrun = 0
database_name = "trivia_test"
if testrun == 0:
    #delete existing test database
    bashCommand = "dropdb {}".format(database_name)
    os.system(bashCommand)
    #setup new test database
    bashCommand = "createdb {}".format(database_name)
    os.system(bashCommand)
    #load test database with example data
    bashCommand = "psql {} < {}.psql".format(database_name, database_name)
    os.system(bashCommand)
    testrun = testrun +1
    print("New test database initialized")
    print("Testrun: {}".format(testrun))
else:
    testrun = testrun +1
    print("Testrun {} with current test database".format(testrun))
    pass