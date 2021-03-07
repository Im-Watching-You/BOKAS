"""
Date: 2019.10.28
Programmer: MH, MC
Description: Code for course
"""
import constants
import pymysql


class Course:
    def __init__(self):
        """
        To initialize object
        """
        self.db_course = DBCourse()
        self.id = None
        self.course_title = None
        self.course_level = None
        self.teaching_methods = None
        self.passing_conditions = None

    def register_course(self, title, level, methods, pass_condition):
        """
        To register course using the data
        :param title: string, course title
        :param level: int, course level
        :param methods: string, teaching methods
        :param pass_condition: string, passing conditions
        :return: boolean, status of registering course
        """
        self.course_title = title
        self.course_level = level
        self.teaching_methods = methods
        self.passing_conditions = pass_condition

        result = self.db_course.register_course(self.course_title, self.course_level,
                                                self.teaching_methods, self.passing_conditions)
        if result:
            self.id = self.retrieve_course(self.course_title, self.course_level, self.teaching_methods,
                                           self.passing_conditions)[0]["id"]
            print(self.id)
        return result

    def modify_course(self, title=None, level=None, methods=None, pass_condition=None):
        """
        To modify course
        :param title: string, title to change
        :param level: int, level to change
        :param methods: teaching methods to change
        :param pass_condition: string, passing conditions to change
        :return: boolean, statues of modifying
        """

        result = self.db_course.modify_course(self.id, title, level, methods, pass_condition)
        if result:                              # if change data can be saved, the object's data will be changed.
            if title is not None:
                self.course_title = title
            if level is not None:
                self.course_level = level
            if methods is not None:
                self.teaching_methods = methods
            if pass_condition is not None:
                self.passing_conditions = pass_condition
        else:
            pass
        return result

    def retrieve_course(self, title=None, level=None, methods=None, pass_condition=None):
        """
        To retrieve course
        :param title: string, title to change
        :param level: int, level to change
        :param methods: teaching methods to change
        :param pass_condition: string, passing conditions to change
        :return: list, retrieved course
        """
        found_course = self.db_course.retrieve_course(self.id, title, level, methods, pass_condition)
        return found_course

    def delete_course(self):
        """
        To delete course
        :return: status of deleting course
        """
        result = self.db_course.delete_course(self.id)
        return result


class DBCourse:
    def __init__(self):
        try:
            self.conn = pymysql.connect(host=constants.HOST_ADDR, user='root', password='root', db='bokas',
                                        charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            self.conn = None

    def register_course(self, title, level, methods, pass_condition):
        """
        To register course using the data
        :param title: string, course title
        :param level: int, course level
        :param methods: string, teaching methods
        :param pass_condition: string, passing conditions
        :return: boolean, status of registering course
        """
        sql = "INSERT INTO course (course_title, course_level, teaching_methods, passing_conditions)" \
              "VALUES (%s, %s, %s, %s)"

        info = (title, level, methods, pass_condition)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, info)
                self.conn.commit()
                return True
        except:
            return False

    def modify_course(self, id, title=None, level=None, methods=None, pass_condition=None):
        """
        To modify course already registered
        :param id: int, course id
        :param title: string, course title
        :param level: int, course level
        :param methods: string, teaching methods
        :param pass_condition: string, passing conditions
        :return: boolean, statues of modifying course
        """
        sql = "UPDATE course SET "

        if title is not None:
            sql += "course_title='"+title+"'"
            if any([level, methods, pass_condition]):
                sql += ", "

        if level is not None:
            sql += "course_level='"+str(level)+"'"
            if any([methods, pass_condition]):
                sql += ", "

        if methods is not None:
            sql += "teaching_methods='"+methods+"'"
            if any([pass_condition]):
                sql += ", "

        if pass_condition is not None:
            sql += "passing_conditions='" + pass_condition + "'"

        sql += " WHERE id="+str(id)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                self.conn.commit()
                return True
        except:
            return False

    def retrieve_course(self, id=None, title=None, level=None, methods=None, pass_condition=None):
        """
        To retrieve courses following input conditions
        :param id: int, course id
        :param title: string, title to change
        :param level: int, level to change
        :param methods: teaching methods to change
        :param pass_condition: string, passing conditions to change
        :return: list, retrieved course
        """
        sql = "SELECT * FROM course"

        if any([id, title, level, methods, pass_condition]):   # if at least one inputs are not none, any() returns true
           sql += " WHERE "

        if id is not None:
            sql += "id=" + str(id)
            if any([title, level, methods, pass_condition]):
                sql += " AND "

        if title is not None:
            sql += "course_title='" + title + "'"
            if any([level, methods, pass_condition]):
                sql += " AND "

        if level is not None:
            sql += "course_level='" + str(level) + "'"
            if any([methods, pass_condition]):
                sql += " AND "

        if methods is not None:
            sql += "teaching_methods='" + methods + "'"
            if any([pass_condition]):
                sql += " AND "

        if pass_condition is not None:
            sql += "passing_conditions='" + pass_condition + "'"

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except:
            return []

    def delete_course(self, id):
        """
        To delete course
        :param id: int, course id
        :return: status of deleting course
        """
        try:
            with self.conn.cursor() as cursor:
                sql = "delete from course where id=%s"
                cursor.execute(sql, id)
                self.conn.commit()
                return True
        except:
            return False


if __name__ == '__main__':
    course = Course()
    dbcourse = DBCourse()
    # print(course.register_course("Test113", 2, 'Test', "Test"))
    # print(dbcourse.modify_course(1, "Testnew", 3, 'Test1', "Test1"))
    # print(course.retrieve_course())
    # print(course.retrieve_course(title="Test"))
    # print(course.retrieve_course(methods="Test"))
    # print(dbcourse.delete_course(10))


