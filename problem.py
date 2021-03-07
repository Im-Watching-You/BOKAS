"""
Date: 2019.10.28
Programmer: MC
Description: code for Problem Management
"""

import random
import pymysql
import numpy as np
from datetime import datetime
from constants import HOST_ADDR, Level


class Problem:
    def __init__(self):
        """
        To initialize object
        """
        self.db_problem = DBProblem()
        self.id = None
        self.problem_name = None
        self.course_id = None
        self.problem_type = None
        self.difficulty_level = None
        self.question_description = None
        self.solution_description = None
        self.solution_interpretation = None
        self.author = None

        self.num_trainees = 10  # Number of trainees
        self.order = []         # List of problems for only one trainee
        self.all_order = []     # List of problems that were used for all trainees
        self.redundancy_rate = None
        self.level_distribution = None
        self.course_distribution = None

        # Autonomous attributes (don't fill them manually)
        self.date_created = None
        self.date_registered = None
        self.revision_history = None

    def register_problem(self, name, course, type, level, question, solution, interpretation, author):
        """
        To register a problem using input information by Author
        :param name: string, the problem name
        :param course: int, the course ID
        :param type: string, the type of problem
        :param level: int, problem’s difficulty level
        :param question: string, description of question
        :param solution: string, description of solution
        :param interpretation: string, interpretation description to a solution for the problem
        :param author: int, author ID
        :return: boolean, status of registering problem
        """
        self.problem_name = name
        self.course_id = course
        self.problem_type = type
        self.difficulty_level = level
        self.question_description = question
        self.solution_description = solution
        self.solution_interpretation = interpretation
        self.author = author

        self.date_created = self.get_current_datetime()
        self.date_registered = self.get_current_datetime()

        # To store the object's data at database; Identifier: author_evaluator=0 (Author = 0; Evaluator = 1)
        result = self.db_problem.register_problem(self.problem_name, self.course_id, self.date_created,
                                                  self.problem_type, self.difficulty_level, self.question_description,
                                                  self.solution_description, self.solution_interpretation,
                                                  self.author, self.date_registered)
        if result:
            self.id = self.choose_problem(self.problem_name, self.course_id, self.date_created,
                                          self.problem_type, self.difficulty_level, self.question_description,
                                          self.solution_description, self.solution_interpretation,
                                          self.author, self.date_registered)[0]["id"]
            print(self.id)
        return result

    def modify_problem(self, name=None, course=None, type=None, level=None, question=None, solution=None,
                       interpretation=None, author=None):
        """
        To modify a problem using input information
        :param name: string, the problem name
        :param course: int, the course ID
        :param type: string, to change the type of problem
        :param level: int, to change problem’s difficulty level
        :param question: string, to change description of question
        :param solution: string, to change description of solution
        :param interpretation: string, to change interpretation description to a solution for the problem
        :param author: int, to change author ID to the one who changed the information
        :return: boolean, status of modifying problem
        """
        # To modify problem in database
        result = self.db_problem.modify_problem(self.id, name, course, type, level, question,
                                                solution, interpretation, author)

        if result:  # if change data can be saved, the object's data will be changed.
            if name is not None:
                self.problem_name = name
            if course is not None:
                self.course_id = course
            if type is not None:
                self.problem_type = type
            if level is not None:
                self.difficulty_level = level
            if question is not None:
                self.question_description = question
            if solution is not None:
                self.solution_description = solution
            if interpretation is not None:
                self.solution_interpretation = interpretation
            if author is not None:
                self.author = author
        else:
            pass
        return result

    def delete_problem(self):
        """
        To delete problem using its ID
        :return: boolean, status of deleting problem
        """
        result = self.db_problem.delete_problem(self.id)
        return result

    def choose_problem(self, name=None, course=None, date_created=None, type=None, level=None,
                       question=None, solution=None, interpretation=None, author=None, date_registered=None):
        """
        To choose problems
        :param name: string, the problem name
        :param course: int, the course ID
        :param date_created: datetime, the date of creating the problem
        :param type: string, the type of problem
        :param level: int, problem’s difficulty level
        :param question: string, description of question
        :param solution: string, description of solution
        :param interpretation: string, interpretation description to a solution for the problem
        :param author: int, author ID
        :param date_registered: datetime, the date of registering the problem
        :return: list, chosen problems
        """
        result = self.db_problem.retrieve_problem(self.id, name, course, date_created, type, level, question, solution,
                                                  interpretation, author, date_registered)
        return result

    def get_problem(self, redundancy_rate=None, course_distribution=None, level_distribution=None):
        """
        To get a one random problem for valuing a trainee
        :param redundancy_rate: float, measures the degree of appearance that a same problem is asked to trainees
        :param level_distribution: list, distribution of problems over the 5 levels of difficulty [60, 5, 10, 5, 20]%
        :param course_distribution: list, the distribution of problems among courses covered [60, 5, 10, 5, 20]%
        :return problem, gotten problem
        """
        self.redundancy_rate = redundancy_rate
        self.course_distribution = course_distribution
        self.level_distribution = level_distribution

        problem_list = self.db_problem.retrieve_problem()   # Get all problems

        # To update list of problems by adding some specifying rules
        result = self.specified_rules(problem_list, redundancy_rate, course_distribution, level_distribution)

        return result

    def enter_problem(self, name, course, type, level, question, solution, interpretation, author):
        """
        To register a problem using input information by Evaluator
        :param name: string, the problem name
        :param course: int, the course ID
        :param type: string, the type of problem
        :param level: int, problem’s difficulty level
        :param question: string, description of question
        :param solution: string, description of solution
        :param interpretation: string, interpretation description to a solution for the problem
        :param author: int, Evaluator ID
        :return: boolean, status of registering problem
        """
        self.problem_name = name
        self.course_id = course
        self.problem_type = type
        self.difficulty_level = level
        self.question_description = question
        self.solution_description = solution
        self.solution_interpretation = interpretation
        self.author = author

        self.date_created = self.get_current_datetime()

        # To store the object's data at database
        result = self.db_problem.register_problem(self.problem_name, self.course_id, self.date_created,
                                                  self.problem_type, self.difficulty_level, self.question_description,
                                                  self.solution_description, self.solution_interpretation, self.author)
        if result:
            self.id = self.choose_problem(self.problem_name, self.course_id, self.date_created,
                                          self.problem_type, self.difficulty_level, self.question_description,
                                          self.solution_description, self.solution_interpretation, self.author)[0]["id"]
            print(self.id)
        return result

    """
    Additional Methods
    """
    def specified_rules(self, list_problem, redundancy_rate=None, course_distribution=None, level_distribution=None):
        """
        To add some specifying rules for list of problems following input conditions
        :param list_problem: list, list of chosen problems
        :param redundancy_rate: float, measures the degree of appearance that a same problem is asked to trainees
        :param level_distribution: list, distribution of problems over the 5 levels of difficulty [60, 5, 10, 5, 20]%
        :param course_distribution: list, the distribution of problems among courses covered [60, 5, 10, 5, 20]%
        :return: list, a new list of chosen problems
        """

        """
            Concept of specified_rules!!!
            1. Use list of problems to filter them by courses!
            2. Choose one course by using weight of course_distribution
            3. Use gotten course to filter it by levels!
            4. Choose one level by using weight of level_distribution
            5. Use gotten level list of problems to get random problem and considering the redundancy_rate
            
            Note: In fact, weights can be any numbers! They can be like this: [60, 120, 9999, 55, 31]
        """
        # We will stop the loop when will find problem which satisfies our filter!
        while True:
            if course_distribution is not None:     # Check do we need use course distribution or not!
                # Define how many courses we have in database and create list with course names
                s = set()
                for l in list_problem:
                    course_id = l['course_id']
                    s.add(course_id)        # If the course ID is unique, it will be saved in the set {1,2,3,4,5...}
                course_ids = list(s)        # Convert to list
                print("Number of courses {0}\nCourse ids: {1}".format(len(course_ids), course_ids))

                # Create multiple list, [[], [], [], [], []] for course distributions it depend on number of courses
                course_list = []
                for i in range(len(course_ids)):
                    course_list.append([])

                # To filter problems by Courses
                for p in list_problem:
                    for k in range(len(course_ids)):
                        # If a problem from the same course, we will save it into course list with its identifier
                        if p['course_id'] == course_ids[k]:
                            course_list[k].append(p)
                            break

                # Show courses. Each course has only its course problems
                for i in range(len(course_list)):
                    print(course_list[i])

                # For course Distribution! Choose a course of problems by weights of courses!
                course = random.choices(course_list, weights=course_distribution, k=1)[0]
                print("Chosen course:\n{0}".format(course))
            else:
                course = list_problem   # If we don't use course distr., then just rename list of problems' to course!

            print('\n/////////////////////////////////////////////////////////////////////////////////////////////\n')

            if level_distribution is not None:  # Check do we need use level distribution or not!
                # Create multiple list, for levels distributions
                level_list = [[], [], [], [], []]   # For each level: 1-5

                # To filter problems in a course by levels
                for p in course:
                    for i in range(5):
                        # If a problem with the same level, we will save it into level list with its identifier
                        if p['difficulty_level'] == i+1:
                            level_list[i].append(p)
                            break

                # Show problems by levels
                for i in range(5):
                    print("Level: {0}\t#: {1}\n{2}".format(i+1, len(level_list[i]), level_list[i]))

                # For Level Distribution (choose a problem by weight of levels)
                level = random.choices(level_list, weights=level_distribution, k=1)[0]
                print("Chosen level:\n{0}".format(level))

                if not level:
                    continue
            else:
                level = course

            print('\n/////////////////////////////////////////////////////////////////////////////////////////////\n')

            # Define how many problems can be the same for different trainees
            if (redundancy_rate is not None) and (self.num_trainees is not None):
                iterations = np.around(self.num_trainees * redundancy_rate)
            else:
                iterations = 0

            # Choose problem by redundancy rate
            while True:
                p = random.choice(level)    # Choose random problem
                # If it's a new problem for a trainee and it hasn't shown more than 'iterations' to other trainees
                if self.order.count(p) == 0 and self.all_order.count(p) <= iterations:
                    self.order.append(p)         # List of unique problems for only one trainee
                    self.all_order.append(p)     # List of problems that were used for all trainees

                    # To subtract the number of iterations if the problem were already used
                    if self.all_order.count(p) != 1 and iterations >= 1:  # all_order.count(p) = 1
                        iterations -= 1
                    break   # Stop the loop when we will find a problem which satisfies requirements
                else:
                    continue

            # If the problem wasn't find because of limited number of problems. Now we have only 20!
            if not self.order[-1]:
                continue
            else:
                break   # Stop the loop when we will find a problem which satisfies requirements

        result = self.order[-1]
        return result

    def get_current_datetime(self):
        """
        To return current time as timestamp
        :return: date
        """
        result = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return result


class DBProblem:
    def __init__(self):
        """
        To connect to Database
        """
        self.revision_history = None

        try:
            self.conn = pymysql.connect(host=HOST_ADDR, user='root', password='root', db='bokas',
                                        charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            self.conn = None

    def register_problem(self, name, course, date_created, type, level, question, solution,
                         interpretation, author, date_registered=None):
        """
        To register a problem using input information
        :param name: string, the problem name
        :param course: int, the course ID
        :param date_created: datetime, the date of creating the problem
        :param type: string, the type of problem
        :param level: int, problem’s difficulty level
        :param question: string, description of question
        :param solution: string, description of solution
        :param interpretation: string, interpretation description to a solution for the problem
        :param author: int, author ID
        :param date_registered: datetime, the date of registering the problem
        :return: boolean, status of registering problem
        """

        sql = "INSERT INTO problem (problem_name, course_id, date_created, problem_type, difficulty_level," \
              " question_description, solution_description, solution_interpretation, author, date_registered)" \
              " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        info = (name, course, date_created, type, level, question, solution,
                interpretation, author, date_registered)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, info)
                self.conn.commit()
                return True
        except:
            return False

    def modify_problem(self, id, name=None, course=None, type=None, level=None, question=None, solution=None,
                       interpretation=None, author=None):
        """
        To modify a problem using input information
        :param id: int, problem ID
        :param name: string, the problem name
        :param course: int, the course ID
        :param type: string, to change the type of problem
        :param level: int, to change problem’s difficulty level
        :param question: string, to change description of question
        :param solution: string, to change description of solution
        :param interpretation: string, to change interpretation description to a solution for the problem
        :param author: int, to change author ID to the one who changed the information
        :return: boolean, status of modifying problem
        """
        # To extract data about revision history to modify history later
        with self.conn.cursor() as cursor:
            sql = "SELECT revision_history FROM problem WHERE id = %s"
            cursor.execute(sql, id)
            self.revision_history = cursor.fetchone()['revision_history']

        sql = "UPDATE problem SET "

        sql += "revision_history='"+self.update_history(self.revision_history)+"'"
        if any([name, course, type, level, question, solution, interpretation, author]):
            sql += ", "

        if name is not None:
            sql += "problem_name='"+name+"'"
            if any([course, type, level, question, solution, interpretation, author]):
                sql += ", "

        if course is not None:
            sql += "course_id='"+str(course)+"'"
            if any([type, level, question, solution, interpretation, author]):
                sql += ", "

        if type is not None:
            sql += "problem_type='"+type+"'"
            if any([level, question, solution, interpretation, author]):
                sql += ", "

        if level is not None:
            sql += "difficulty_level='"+str(level)+"'"
            if any([question, solution, interpretation, author]):
                sql += ", "

        if question is not None:
            sql += "question_description='"+question+"'"
            if any([solution, interpretation, author]):
                sql += ", "

        if solution is not None:
            sql += "solution_description='"+solution+"'"
            if any([interpretation, author]):
                sql += ", "

        if interpretation is not None:
            sql += "solution_interpretation='"+interpretation+"'"
            if any([author]):
                sql += ", "

        if author is not None:
            sql += "author='"+str(author)+"'"

        sql += " WHERE id="+str(id)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                self.conn.commit()
                return True
        except:
            return False

    def retrieve_problem(self, id=None, name=None, course=None, date_created=None, type=None, level=None,
                         question=None, solution=None, interpretation=None, author=None, date_registered=None):
        """
        To retrieve problems following input conditions
        :param id: int, problem ID
        :param name: string, the problem name
        :param course: int, the course ID
        :param date_created: datetime, the date of creating the problem
        :param type: string, the type of problem
        :param level: int, problem’s difficulty level
        :param question: string, description of question
        :param solution: string, description of solution
        :param interpretation: string, interpretation description to a solution for the problem
        :param author: int, author ID
        :param date_registered: datetime, the date of registering the problem
        :return: list, retrieved problems
        """
        sql = "SELECT * FROM problem"

        # If at least one parameter are not none, any() returns True
        if any([id, name, course, date_created, type, level, question, solution, interpretation, author, date_registered]):
           sql += " WHERE "

        if id is not None:
            sql += "id='"+str(id)+"'"
            if any([name, course, date_created, type, level, question, solution, interpretation, author, date_registered]):
                sql += " AND "

        if name is not None:
            sql += "problem_name='"+name+"'"
            if any([course, date_created, type, level, question, solution, interpretation, author, date_registered]):
                sql += " AND "

        if course is not None:
            sql += "course_id='"+str(course)+"'"
            if any([date_created, type, level, question, solution, interpretation, author, date_registered]):
                sql += " AND "

        if date_created is not None:
            sql += "date_created='"+date_created+"'"
            if any([type, level, question, solution, interpretation, author, date_registered]):
                sql += " AND "

        if type is not None:
            sql += "problem_type='"+type+"'"
            if any([level, question, solution, interpretation, author, date_registered]):
                sql += " AND "

        if level is not None:
            sql += "difficulty_level='"+str(level)+"'"
            if any([question, solution, interpretation, author, date_registered]):
                sql += " AND "

        if question is not None:
            sql += "question_description='"+question+"'"
            if any([solution, interpretation, author, date_registered]):
                sql += " AND "

        if solution is not None:
            sql += "solution_description='"+solution+"'"
            if any([interpretation, author, date_registered]):
                sql += " AND "

        if interpretation is not None:
            sql += "solution_interpretation='"+interpretation+"'"
            if any([author, date_registered]):
                sql += " AND "

        if author is not None:
            sql += "author='"+str(author)+"'"
            if any([date_registered]):
                sql += " AND "

        if date_registered is not None:
            sql += "date_registered='"+date_registered+"'"

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except:
            return []

    def delete_problem(self, id):
        """
        To delete problem using its ID
        :param id: int, problem ID
        :return: boolean, status of deleting problem
        """
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM problem WHERE id=%s"
                cursor.execute(sql, id)
                self.conn.commit()
                return True
        except:
            return False

    """
    Additional Methods
    """
    def get_current_datetime(self):
        """
        To return current time as timestamp
        :return: date
        """
        result = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return result

    def update_history(self, previous_dates):
        """
        To update revision_history
        :param previous_dates: str, current information about revision_history
        :return updated revision_history: str, for example: 2019-10-11 16:50:13; 2019-10-11 16:50:45; ...
        """
        current_date = str(self.get_current_datetime())
        if previous_dates is not None:
            return previous_dates + '; ' + current_date
        else:
            return current_date


if __name__ == '__main__':
    problem = Problem()
    dbproblem = DBProblem()

    name_c = "OOAD-101. Inheritance (1)"
    course_c = 2
    type_c = "True/False"
    level_c = Level.LOW_MEDIUM.value
    question_c = "It can inherit attributes!"
    solution_c = "True"
    interpretation_c = "The system can inherit attributes"
    author_c = 101

    # problem.register_problem(name_c, course_c, type_c, level_c, question_c, solution_c, interpretation_c, author_c)

    # dbproblem.modify_problem(id=113, name="OOAD-99. Inheritance (2)", course=3, type="Multiple Questions", level=1,
    #                          question='Addition, Subtraction, Multiplication, Division',
    #                          solution='Addition, Multiplication', interpretation='Only + and /', author=100)

    # print(problem.choose_problem())
    # print(problem.choose_problem(level="1"))
    # print(dbproblem.retrieve_problem(id=9))

    # print(dbproblem.delete_problem(id=8))

    # rate = 0.2
    # weights_cor = [20, 10, 5, 60, 5]
    # weights_lev = [10, 20, 40, 20, 10]
    # print(problem.get_problem(redundancy_rate=rate, course_distribution=weights_cor, level_distribution=weights_lev))

    # problem.enter_problem(name_c, course_c, type_c, level_c, question_c, solution_c, interpretation_c, author_c)
