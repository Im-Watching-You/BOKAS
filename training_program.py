"""
Date: 2019.10.22
Programmer: MC
Description: code for Training Program Management
"""
import pymysql
from datetime import datetime
from constants import HOST_ADDR, Level, Conditions


class TrainingProgram:
    def __init__(self):
        """
        To initialize object
        """
        self.id = None
        self.program_name = None
        self.program_start_date = None
        self.program_level = None
        self.training_duration = None
        self.courses = None
        self.offering_conditions = None
        self.db_training_program = DBTrainingProgram()

    def register_training_program(self, name, start_date, level, duration, courses, condition):
        """
        To register training program
        :param name: string, the training program name
        :param start_date: datetime, the date of beginning the training program
        :param level: int, difficulty level of training program
        :param duration: int, training program duration in days
        :param courses: list, list of courses in the training program
        :param condition: string, training program status
        :return: boolean, status of registering training program
        """
        self.program_name = name
        self.program_start_date = start_date
        self.program_level = level
        self.training_duration = duration
        self.courses = courses
        self.offering_conditions = condition

        courses = self._convert_list_to_str(courses)
        result = self.db_training_program.register_training_program(self.program_name, self.program_start_date,
                                                                    self.program_level, self.training_duration,
                                                                    courses, self.offering_conditions)
        if result:
            self.id = self.retrieve_training_program(self.program_name, self.program_start_date, self.program_level,
                                                     self.training_duration, courses,
                                                     self.offering_conditions)[0]["id"]
            print(self.id)
        return result

    def modify_training_program(self, name=None, start_date=None, level=None, duration=None,
                                courses=None, condition=None):
        """
        To modify training program
        :param name: string, to change a training program name
        :param start_date: datetime, to change the date of beginning the training program
        :param level: int, to change difficulty level of training program
        :param duration: int, to change training program duration in days
        :param courses: list, to change list of courses in the training program
        :param condition: string, to change training program status
        :return: boolean, status of modifying training program
        """
        if courses is not None:
            courses = self._convert_list_to_str(courses)

        result = self.db_training_program.modify_training_program(self.id, name, start_date, level,
                                                                  duration, courses, condition)

        if result:  # if change data can be saved, the object's data will be changed.
            if name is not None:
                self.program_name = name
            if start_date is not None:
                self.program_start_date = start_date
            if level is not None:
                self.program_level = level
            if duration is not None:
                self.training_duration = duration
            if courses is not None:
                self.courses = self._convert_str_to_list(courses)
            if condition is not None:
                self.offering_conditions = condition
        else:
            pass

        return result

    def retrieve_training_program(self, name=None, start_date=None, level=None, duration=None,
                                  courses=None, condition=None):
        """
        To retrieve training program following input conditions
        :param name: string, the training program name
        :param start_date: datetime, the date of beginning the training program
        :param level: int, difficulty level of training program
        :param duration: int, training program duration in days
        :param courses: list, list of courses in the training program
        :param condition: string, training program status
        :return: list, retrieved training programs
        """
        if courses is not None:
            courses = self._convert_list_to_str(courses)

        result = self.db_training_program.retrieve_training_program(self.id, name, start_date, level,
                                                                    duration, courses, condition)
        return result

    def delete_training_program(self):
        """
        To delete a training program using its ID
        :return: boolean, status of deleting the training program
        """
        result = self.db_training_program.delete_training_program(self.id)
        return result

    def _convert_list_to_str(self, l):
        """
        To convert list to string having ','
        :param l: list, target list
        :return: string
        """
        if type(l) is not str:
            for i in range(len(l)):
                l[i] = str(l[i])
            result = ', '.join(l)
        else:
            result = l
        return result

    def _convert_str_to_list(self, t):
        """
        To convert string to list
        :param t: string, target string having ','
        :return: list
        """
        if type(t) is not list:
            result = t.split(', ')
        else:
            result = t
        return result


class DBTrainingProgram:
    def __init__(self):
        """To connect to Database"""
        try:
            self.conn = pymysql.connect(host=HOST_ADDR, user='root', password='root', db='bokas',
                                        charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            self.conn = None

    def register_training_program(self, name, start_date, level, duration, courses, condition):
        """
        To register training program
        :param name: string, the training program name
        :param start_date: datetime, the date of beginning the training program
        :param level: int, difficulty level of training program
        :param duration: int, training program duration in days
        :param courses: list, list of courses in the training program
        :param condition: string, training program status
        :return: boolean, status of registering training program
        """
        sql = "INSERT INTO training_program (program_name, program_start_date, program_level, training_duration," \
              " courses, offering_conditions) VALUES (%s, %s, %s, %s, %s, %s)"

        info = (name, start_date, level, duration, courses, condition)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, info)
                self.conn.commit()
                return True
        except:
            return False

    def modify_training_program(self, id, name, start_date, level, duration, courses, condition):
        """
        To modify training program
        :param id: int, training program ID
        :param name: string, to change a training program name
        :param start_date: datetime, to change the date of beginning the training program
        :param level: int, to change difficulty level of training program
        :param duration: int, to change training program duration in days
        :param courses: list, to change list of courses in the training program
        :param condition: string, to change training program status
        :return: boolean, status of modifying training program
        """
        sql = "UPDATE training_program SET "

        if name is not None:
            sql += "program_name='" + name + "'"
            if any([start_date, level, duration, courses, condition]):
                sql += ", "

        if start_date is not None:
            sql += "program_start_date='{0}'".format(start_date)
            if any([level, duration, courses, condition]):
                sql += ", "

        if level is not None:
            sql += "program_level='" + str(level) + "'"
            if any([duration, courses, condition]):
                sql += ", "

        if duration is not None:
            sql += "training_duration='" + str(duration) + "'"
            if any([courses, condition]):
                sql += ", "

        if courses is not None:
            sql += "courses='" + courses + "'"
            if any([condition]):
                sql += ", "

        if condition is not None:
            sql += "offering_conditions='" + condition + "'"

        sql += " WHERE id=" + str(id)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                self.conn.commit()
                return True
        except:
            return False

    def retrieve_training_program(self, id, name, start_date, level, duration, courses, condition):
        """
        To retrieve training program following input conditions
        :param id: int, training program ID
        :param name: string, the training program name
        :param start_date: datetime, the date of beginning the training program
        :param level: int, difficulty level of training program
        :param duration: int, training program duration in days
        :param courses: list, list of courses in the training program
        :param condition: string, training program status
        :return: list, retrieved training programs
        """
        sql = "SELECT * FROM training_program"

        # If at least one parameter are not none, any() returns True
        if any([id, name, start_date, level, duration, courses, condition]):
           sql += " WHERE "

        if id is not None:
            sql += "id='"+str(id)+"'"
            if any([name, start_date, level, duration, courses, condition]):
                sql += " AND "

        if name is not None:
            sql += "program_name='"+name+"'"
            if any([start_date, level, duration, courses, condition]):
                sql += " AND "

        if start_date is not None:
            sql += "program_start_date='{0}'".format(start_date)
            if any([level, duration, courses, condition]):
                sql += " AND "

        if level is not None:
            sql += "program_level='"+str(level)+"'"
            if any([duration, courses, condition]):
                sql += " AND "

        if duration is not None:
            sql += "training_duration='"+str(duration)+"'"
            if any([courses, condition]):
                sql += " AND "

        if courses is not None:
            sql += "courses='"+str(courses)+"'"
            if any([condition]):
                sql += " AND "

        if condition is not None:
            sql += "offering_conditions='"+condition+"'"

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                program_list = cursor.fetchall()
                return program_list
        except:
            return []

    def delete_training_program(self, id):
        """
        To delete a training program using its ID
        :param id: int, the training program ID
        :return: boolean, status of deleting the training program
        """
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM training_program WHERE id=%s"
                cursor.execute(sql, id)
                self.conn.commit()
                return True
        except:
            return False


if __name__ == '__main__':
    # Initialise Classes
    program = TrainingProgram()
    dbProgram = DBTrainingProgram()

    # Initialise variables for register
    name_tt = 'Associate Architect'
    start_date_tt = '2019-10-25 08:30:00'
    start_date_tt = datetime.strptime(start_date_tt, '%Y-%m-%d %H:%M:%S')   # convert to datetime
    level_tt = Level.LOW_MEDIUM.value
    duration_tt = 364
    courses_tt = ['Class Diagram', 'Use Case Diagram', 'Behavior Diagram']
    condition_tt = Conditions.WAITING.value

    # Initialise variables for modifying
    name_ttt = 'Public Architect'
    start_date_ttt = '2019-08-23 09:30:00'
    start_date_ttt = datetime.strptime(start_date_ttt, '%Y-%m-%d %H:%M:%S')  # convert to datetime
    level_ttt = Level.MEDIUM.value
    duration_ttt = 653
    courses_ttt = ['New Diagram', 'Old Diagram', 'Just Diagram']
    condition_ttt = Conditions.STARTED.value

    # Testing
    # print(program.register_training_program(name_tt, start_date_tt, level_tt, duration_tt, courses_tt, condition_tt))
    # print(program.modify_training_program(7, name_ttt, start_date_ttt, level_ttt,
    #                                       duration_ttt, courses_ttt, condition_ttt))

    # program_list = program.retrieve_training_program()
    # for i in program_list:
    #     print(i)

    # print(dbProgram.delete_training_program(4))
