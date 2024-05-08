import pymysql
import pandas as pd
import sys

lastid = 0

class lyymysql_class():

    def __init__(self, conn):
        self.conn = conn

    def create_mysql_table(self, conn, table_name, debug=False):
        sqlquery = "CREATE TABLE if not exists `" + table_name + "` (`id` INT NOT NULL AUTO_INCREMENT,\
            `code` VARCHAR(9) NULL ,\
            `day` DATE NOT NULL,\
            `open` DECIMAL(6,2) NOT NULL,\
            `high` DECIMAL(6,2) NOT NULL,\
            `close` DECIMAL(6,2) NOT NULL,\
            `low` DECIMAL(6,2) NOT NULL,\
            `volume` DECIMAL(16,0) NOT NULL,\
            `up` DECIMAL(6,2) NULL,\
            `tenhigh` DECIMAL(6,2) NULL,\
            `chonggao` DECIMAL(6,2) NULL,\
            `huitoubo` DECIMAL(6,2) NOT NULL,\
            `notfull` INT NULL,\
            PRIMARY KEY(`id`),\
           UNIQUE INDEX `uk_day_code`(`code`,`day`))  \
                ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"

        cursor = self.conn.cursor()
        cursor.execute(sqlquery)
        cursor.close()

    def df插入入mysql(self, df):
        table_name = 'stock_all_codes'
        # define the columns to be inserted
        columns = ['code', 'name', 'tradeStatus', 'ipoDate']

        # loop through each row in the dataframe
        for index, row in df.iterrows():
            # check if the code already exists in the table
            query = f"SELECT * FROM {table_name} WHERE code = '{row['code']}'"
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            # if the code exists, update the tradeStatus column
            if len(result) > 0:
                update_query = f"UPDATE {table_name} SET tradeStatus = {row['tradeStatus']} WHERE code = '{row['code']}'"
                cursor.execute(update_query)
            # if the code does not exist, insert a new row
            else:
                insert_query = f"INSERT INTO {table_name} (code, name, tradeStatus, ipoDate) VALUES ('{row['code']}', '{row['code_name']}', {row['tradeStatus']}, '{row['ipodate']}')"
                cursor.execute(insert_query)

        self.conn.commit()
        cursor.close()

    def get_tdx_server_list(self):
        query = "SELECT ip FROM stock_tdx_server"
        df = pd.read_sql(query, self.conn)
        return df.ip.to_list()

    def 获取股票代码表(self, debug=False):
        if debug: print(sys._getframe().f_code.co_name)
        query = "SELECT code FROM stock_all_codes"
        df = pd.read_sql(query, self.conn)
        code_list = df['code'].tolist()
        if debug: print("code_list:", len(code_list))
        return code_list, df

    def get_date_list_mysql(self):
        query = "SELECT day FROM stock_trade_calendars"
        df = pd.read_sql(query, self.conn)
        date_list = df['day'].tolist()
        return date_list

    def get_list_from_sql(self, table_name, column_name, codition=None):
        """
        直接读取数据库中的table_name表中的column_name列，返回list
        """

        if not codition:
            query = f"SELECT {column_name} FROM {table_name}"
        else:
            query = f"SELECT {column_name} FROM {table_name} WHERE {codition}"
        df = pd.read_sql(query, self.conn)
        return_list = df[column_name].tolist()
        return return_list, df

    def search_keyword(self, stk_code, company):
        cursor = self.conn.cursor()
        company = company.replace("股份", "").replace("科技", "").replace("控股", "").replace("集团", "").replace("信息", "").replace("电子", "").replace("环保", "")
        sql = "SELECT * FROM message WHERE (message LIKE '%" + stk_code + "%'" + " OR message LIKE '%" + company + "%') AND time >= DATE_SUB(NOW(), INTERVAL 3 DAY) order by time desc limit 40"
        print("sql:", sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        return_data = ""
        for row in results:
            print(row)
            msg = row[5].replace("\n\n", "\n").replace("\n\n\n", "\n")
            return_data += str(row[1]) + " " + row[3] + "：" + msg + "\n"
        cursor.close()

        return return_data

    def insert_mysql_multi(self, fulldf, db_last_date_int, code_str6):
        pass

    def insert_mysql(self, wmdf, start_date, stk_code_num):
        print("enter insert_mysql")
        sqlquery2 = "day>" + str(start_date)
        newdf = wmdf.query(sqlquery2)
        结果长度 = len(newdf)
        if 结果长度 > 0:
            print(结果长度)
            inserted_rows = self.mysql_insert(newdf, stk_code_num, output=True)
            return (inserted_rows)
        else:
            print("需要插入的数据条数为" + str(结果长度))
        return 0

    def mysql_insert(self, df, table_name, output=True):
        inserted_rows = 0
        # 检查表是否存在,如果不存在则创建
        cursor = self.conn.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()

        if not result:
            self.create_mysql_table(self.conn, table_name)
            inserted_rows = df.shape[0]
            df.to_sql(table_name, self.conn, index=False)
        else:
            # 逐行比较DataFrame和表
            for row in df.iterrows():
                index = row[0]
                value = row[1]
                # 通过SQL查询获取表对应行
                query = f"SELECT * FROM `{table_name}` WHERE {df.columns[0]}={int(value[0])}"
                try:
                    current_row = pd.read_sql(query, self.conn)
                except:
                    dtypes = {0: 'int', 1: 'int', 2: 'int', 3: 'int', 4: 'int', 5: 'int', 6: 'float', 7: 'float', 8: 'float', 9: 'float', 10: 'int'}
                    current_row = pd.DataFrame(columns=['day', 'open', 'high', 'low', 'close', 'volume', 'tenhigh', 'up', 'chonggao', 'huitoubo', 'notfull'])  # 空DataFrame代替空表
                # 比较DataFrame行和表对应行
                print("table_name:", table_name)
                print("-----------------------")
                print(df.loc[index], type(df.loc[index]))
                # df.reset_index(drop=True, inplace=True)
                if current_row.empty:
                    # 表无对应行,插入新行
                    print(df.iloc[index])
                    df.iloc[index].to_sql(table_name, self.conn, index=False, if_exists='replace')
                    inserted_rows += 1  # 计算插入行数
                elif not value.eq(current_row.loc[0]).all():
                    # DataFrame和表对应行不同,更新表行
                    df.iloc[index].to_sql(table_name, self.conn, index=False, if_exists='replace')
                    inserted_rows += 1  # 计算插入行数

        if output:
            print(f'Finished loading {table_name}! Inserted {inserted_rows} rows.')
        cursor.close()
        return inserted_rows


if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', password='password', database='your_database')
    mysql = lyymysql_class(conn)
