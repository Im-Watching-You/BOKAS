"""
Date: 2019.10.23
Programmer: MC
Description: code for Program Offering Management
"""
import pymysql
from datetime import datetime
from constants import HOST_ADDR, Conditions


class ProgramOffering:
    def __init__(self):
        """
        To initialize object
        """
        self.id = None
        self.program_offering_name = None
        self.offering_start_date = None
        self.max_trainees = None
        self.min_trainers = None
        self.program_status = None
        self.db_program_offering = DBProgramOffering()

    def register_offered_program(self, name, start_date, max_trainees, min_trainers, status):
        """
        To register offered program
        :param name: string, the offered program name
        :param start_date: datetime, the date of beginning of the offered program
        :param max_trainees: int, the maximum number of trainees
        :param min_trainers: int, the minimum number of trainers
        :param status: string, offered program status
        :return: boolean, registration status of the offered program
        """
        self.program_offering_name = name
        self.offering_start_date = start_date
        self.max_trainees = max_trainees
        self.min_trainers = min_trainers
        self.program_status = status

        result = self.db_program_offering.register_offered_program(self.program_offering_name, self.offering_start_date,
                                                                   self.max_trainees, self.min_trainers,
                                                                   self.program_status)
        if result:
            self.id = self.retrieve_offered_program(self.program_offering_name, self.offering_start_date,
                                                    self.max_trainees, self.min_trainers, self.program_status)[0]["id"]
            print(self.id)
        return result

    def modify_offered_program(self, name=None, start_date=None, max_trainees=None, min_trainers=None, status=None):
        """
        To modify offered program
        :param name: string, to change the offered program name
        :param start_date: datetime, to change the date of beginning of the offered program
        :param max_trainees: int, to change the maximum number of trainees
        :param min_trainers: int, to change the minimum number of trainers
        :param status: string, to change offered program status
        :return: boolean, modification status of the offered program
        """
        result = self.db_program_offering.modify_offered_program(self.id, name, start_date, max_trainees,
                                                                 min_trainers, status)

        if result:  # if change data can be saved, the object's data will be changed.
            if name is not None:
                self.program_offering_name = name
            if start_date is not None:
                self.offering_start_date = start_date
            if max_trainees is not None:
                self.max_trainees = max_trainees
            if min_trainers is not None:
                self.min_trainers = min_trainers
            if status is not None:
                self.program_status = status
        else:
            pass

        return result

    def retrieve_offered_program(self, name=None, start_date=None, max_trainees=None, min_trainers=None, status=None):
        """
        To retrieve offered programs
        :param name: string, the offered program name
        :param start_date: datetime, the date of beginning of the offered program
        :param max_trainees: int, the maximum number of trainees
        :param min_trainers: int, the minimum number of trainers
        :param status: string, offered program status
        :return: list, retrieved offered programs
        """
        result = self.db_program_offering.retrieve_offered_program(self.id, name, start_date, max_trainees,
                                                                   min_trainers, status)
        return result

    def delete_offered_program(self):
        """
        To delete a offered program using its ID
        :return: boolean, deletion status of the offered program
        """
        result = self.db_program_offering.delete_offered_program(self.id)
        return result


class DBProgramOffering:
    def __init__(self):
        """To connect to Database"""
        try:
            self.conn = pymysql.connect(host=HOST_ADDR, user='root', password='root', db='bokas',
                                        charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            self.conn = None

    def register_offered_program(self, name, start_date, max_trainees, min_trainers, status):
        """
        To register offered program
        :param name: string, the offered program name
        :param start_date: datetime, the date of beginning of the offered program
        :param max_trainees: int, the maximum number of trainees
        :param min_trainers: int, the minimum number of trainers
        :param status: string, offered program status
        :return: boolean, registration status of the offered program
        """
        sql = "INSERT INTO program_offering (program_offering_name, offering_start_date," \
              " max_trainees, min_trainers, program_status) VALUES (%s, %s, %s, %s, %s)"

        info = (name, start_date, max_trainees, min_trainers, status)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, info)
                self.conn.commit()
                return True
        except:
            return False

    def modify_offered_program(self, id, name, start_date, max_trainees, min_trainers, status):
        """
        To modify offered program
        :param id: int, offered program ID
        :param name: string, to change the offered program name
        :param start_date: datetime, to change the date of beginning of the offered program
        :param max_trainees: int, to change the maximum number of trainees
        :param min_trainers: int, to change the minimum number of trainers
        :param status: string, to change offered program status
        :return: boolean, modification status of the offered program
        """
        sql = "UPDATE program_offering SET "

        if name is not None:
            sql += "program_offering_name='" + name + "'"
            if any([start_date, max_trainees, min_trainers, status]):
                sql += ", "

        if start_date is not None:
            sql += "offering_start_date='{0}'".format(start_date)
            if any([max_trainees, min_trainers, status]):
                sql += ", "

        if max_trainees is not None:
            sql += "max_trainees='" + str(max_trainees) + "'"
            if any([min_trainers, status]):
                sql += ", "

        if min_trainers is not None:
            sql += "min_trainers='" + str(min_trainers) + "'"
            if any([status]):
                sql += ", "

        if status is not None:
            sql += "program_status='" + status + "'"

        sql += " WHERE id=" + str(id)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                self.conn.commit()
                return True
        except:
            return False

    def retrieve_offered_program(self, id, name, start_date, max_trainees, min_trainers, status):
        """
        To retrieve offered programs
        :param id: int, offered program ID
        :param name: string, the offered program name
        :param start_date: datetime, the date of beginning of the offered program
        :param max_trainees: int, the maximum number of trainees
        :param min_trainers: int, the minimum number of trainers
        :param status: string, offered program status
        :return: list, retrieved offered programs
        """
        sql = "SELECT * FROM program_offering"

        # If at least one parameter are not none, any() returns True
        if any([id, name, start_date, max_trainees, min_trainers, status]):
           sql += " WHERE "

        if id is not None:
            sql += "id='"+str(id)+"'"
            if any([name, start_date, max_trainees, min_trainers, status]):
                sql += " AND "

        if name is not None:
            sql += "program_offering_name='"+name+"'"
            if any([start_date, max_trainees, min_trainers, status]):
                sql += " AND "

        if start_date is not None:
            sql += "offering_start_date='{0}'".format(start_date)
            if any([max_trainees, min_trainers, status]):
                sql += " AND "

        if max_trainees is not None:
            sql += "max_trainees='"+str(max_trainees)+"'"
            if any([min_trainers, status]):
                sql += " AND "

        if min_trainers is not None:
            sql += "min_trainers='"+str(min_trainers)+"'"
            if any([status]):
                sql += " AND "

        if status is not None:
            sql += "program_status='"+status+"'"

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                program_list = cursor.fetchall()
                return program_list
        except:
            return []

    def delete_offered_program(self, id):
        """
        To delete a offered program using its ID
        :param id: int, offered program ID
        :return: boolean, deletion status of the offered program
        """
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM program_offering WHERE id=%s"
                cursor.execute(sql, id)
                self.conn.commit()
                return True
        except:
            return False


if __name__ == '__main__':
    # Initialise Classes
    program = ProgramOffering()
    dbProgram = DBProgramOffering()

    # Initialise variables for register
    name_t = 'AA2019-05'
    start_date_t = '2019-11-01 08:30:00'
    start_date_t = datetime.strptime(start_date_t, '%Y-%m-%d %H:%M:%S')   # convert to datetime
    max_trainees_t = 35
    min_trainers_t = 2
    program_status_t = Conditions.WAITING.value

    # Initialise variables for modifying
    name_tt = 'AA2019-04(2)'
    start_date_tt = '2022-05-01 09:30:00'
    start_date_tt = datetime.strptime(start_date_tt, '%Y-%m-%d %H:%M:%S')   # convert to datetime
    max_trainees_tt = 60
    min_trainers_tt = 1
    program_status_tt = Conditions.PAUSED.value

    # Testing
    # print(program.register_offered_program(name_t, start_date_t, max_trainees_t, min_trainers_t, program_status_t))
    # print(dbProgram.modify_offered_program(4, name_tt, start_date_tt, max_trainees_tt, min_trainers_tt,
    #                                        program_status_tt))

    # program_list = program.retrieve_offered_program()
    # for i in program_list:
    #     print(i)

    # print(dbProgram.delete_offered_program(4))
