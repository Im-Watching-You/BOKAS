"""
Date: 2019. 10. 10
Programmer: MH
Description: code for Test Session
"""
import constants
import pymysql
import datetime


class TestSessionManager:
    """
    Class for Test session management
    """
    def __init__(self):

        try:
            self.conn = pymysql.connect(host=constants.HOST_ADDR, user='root', password='root', db='bokas',
                                   charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            self.conn = None

    def register_test_session(self, data_cond, courses, duration, dist_prob, dist_diff, num_evaluator, redundancy_rate):
        """
        To register test session using input information
        :param data_cond:
        :param courses:
        :param duration:
        :param dist_prob:
        :param dist_diff:
        :param num_evaluator:
        :param redundancy_rate:
        :return:
        """
        sql = "INSERT INTO test_session (data_created, data_conducted, courses_covered, time_duration," \
              " dist_problem, dist_difficulty, num_evaluators, eval_ids, represent_eval, redundancy_rate)" \
              " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        dist_diff = self._convert_list_to_str(dist_diff)
        eval_ids = self._convert_list_to_str(num_evaluator)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (self._get_current_time(), data_cond, courses, duration, dist_prob, dist_diff,
                                     len(num_evaluator), eval_ids, "Name", redundancy_rate))
            self.conn.commit()
            return True
        except:
            return False

    def modify_test_session(self, id, data_cond=None, courses=None, duration=None, dist_prob=None, dist_diff=None,
                            num_evaluator=None, redundancy_rate=None, mode=None):
        """
        To modify test session
        :param id:
        :param data_cond:
        :param courses:
        :param duration:
        :param dist_prob:
        :param dist_diff:
        :param num_evaluator:
        :param redundancy_rate:
        :return:
        """
        try:
            with self.conn.cursor() as cursor:
                sql = "UPDATE from 'test_session' where id=%s"
                cursor.execute(sql, id)
                self.conn.commit()
                return True
        except:
            return False

    def retrieve_test_session(self, conditions):
        """
        To retrieve test session
        :param conditions: dict, set of conditions to use when retrieving test session
        :return: list of test sessions
        """
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM test_session"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
        except:
            self.conn.close()

    def delete_test_session(self, id):
        """
        To delete generated test session
        :return: boolean
        """
        try:
            with self.conn.cursor() as cursor:
                sql = "delete from test_session where id=%s"
                cursor.execute(sql, id)
                self.conn.commit()
                return True
        except:
            return False

    def _get_current_time(self):
        """
        To return current time as timestamp
        :return:
        """
        return datetime.datetime.now()

    def _convert_list_to_str(self, l):
        """
        To convert list to string having ','
        :param l: list, target list
        :return: string
        """
        if type(l[0]) is not str:
            for i in range(len(l)):
                l[i] = str(l[i])
        return ','.join(l)

    def _convert_str_to_list(self, t):
        """
        To convert string to list
        :param t: string, target string having ','
        :return: list
        """
        return t.split(',')

    def select_problem_mode(self, s_id, mode):
        self.modify_test_session(id=s_id, mode=mode)

if __name__ == '__main__':
    ts = TestSessionManager()
    print(ts.register_test_session("", 3, "Duration", 0.5, [0.1, 0.2, 0.3, 0.2, 0.2], [1, 2, 3], 0.2))
    ts.retrieve_test_session(None)
    print(ts.delete_test_session(1))