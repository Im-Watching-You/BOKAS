"""
Date: 2019. 10. 10
Programmer: MH
Description: code for Test Item
"""
from constants import HOST_ADDR
import pymysql
import datetime


class TestItem:
    def __init__(self):
        try:
            self.conn = pymysql.connect(host=HOST_ADDR, user='root', password='root', db='bokas',
                                        charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            self.conn = None

    def register_test_item(self, test_session_id, trainee_id, evaluator_id, problem_id, answer, score, comment):
        """
        To register test item
        :param test_session_id:
        :param trainee_id:
        :param evaluator_id:
        :param problem_id:
        :param answer:
        :param score:
        :param comment:
        :return:
        """
        sql = "INSERT INTO test_item (created_time, test_session_id, trainee_id, evaluator_id, problem_id," \
              " trainee_answer, test_score, comment)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (self.get_current_time(), test_session_id, trainee_id, evaluator_id, problem_id,
                                     answer, score, comment))
            self.conn.commit()
            return True
        except:
            return False

    def modify_test_item(self, id, answer=None, score=None, comment=None):
        """
        To modify answer, score, comment in registered test item
        :param id: int, test item's id
        :param answer: string, answer to change
        :param score: int, score to change
        :param comment: string, comment to change
        :return:
        """
        try:
            with self.conn.cursor() as cursor:
                sql = "UPDATE test_item SET "
                if answer is not None:
                    sql += "trainee_answer='"+answer+"'"
                    if any([score, comment]):
                        sql +=", "
                if score is not None:
                    sql += "test_score="+str(score)
                    if comment is not None:
                        sql +=", "
                if comment is not None:
                    sql += "comment='" + comment+"'"
                sql += " WHERE id="+str(id)
                cursor.execute(sql)
                self.conn.commit()
                return True
        except:
            return False

    def retrieve_test_items(self, test_session_id, trainee_id, evaluator_id, problem_id, answer, score, comment):
        try:
            sql = "SELECT * FROM test_item"
            if any([test_session_id, trainee_id, evaluator_id, problem_id, answer, score, comment]):
                sql += " WHERE "
            if test_session_id is not None:
                sql += "test_session_id="+test_session_id
                if any([trainee_id, evaluator_id, problem_id, answer, score, comment]):
                    sql += " , "
            if trainee_id is not None:
                sql += "trainee_id="+trainee_id
                if any([evaluator_id, problem_id, answer, score, comment]):
                    sql += " , "
            if evaluator_id is not None:
                sql += "evaluator_id=" + evaluator_id
                if any([problem_id, answer, score, comment]):
                    sql += " , "
            if problem_id is not None:
                sql += "problem_id=" + problem_id
                if any([answer, score, comment]):
                    sql += " , "
            if answer is not None:
                sql += "trainee_answer='" + answer+"'"
                if any([score, comment]):
                    sql += " , "
            if score is not None:
                sql += "test_score=" + evaluator_id
                if any([comment]):
                    sql += " , "
            if comment is not None:
                sql += "comment='" + comment +"'"

            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
        except:
            self.conn.close()

    def delete_test_item(self, id):
        """
        To delete generated test session
        :return: boolean
        """
        try:
            with self.conn.cursor() as cursor:
                sql = "delete from test_item where id=%s"
                cursor.execute(sql, id)
                self.conn.commit()
                return True
        except:
            return False

    def get_current_time(self):
        """
        To return current time as timestamp
        :return:
        """
        return datetime.datetime.now()

if __name__ == '__main__':
    ti = TestItem()
    ti.register_test_item(2,4,2,1,"HI!", 50, "Not Good")
    ti.modify_test_item(1, score=80)
    ti.modify_test_item(2, answer="It is Test Data.", score=80)
    ti.retrieve_test_items(None)
    ti.delete_test_item(2)
    ti.retrieve_test_items(None)
