import psycopg2

class DBUtils:

    def __init__(self):
        # Provide db connection details
        self.t_host = "localhost" 
        self.t_port = "5432" 
        self.t_dbname = "postgres"
        self.t_user = "postgres"
        self.t_pw = ""

        #### Creating database connection
        self.db_conn = psycopg2.connect(host=self.t_host, port=self.t_port, dbname=self.t_dbname, user=self.t_user, password=self.t_pw)
        self.db_cursor = self.db_conn.cursor()
        self.db_cursor.execute('select version()')
        self.db_cursor.execute('''create table if not exists q_state_player(state varchar(500), q_value varchar(500))''')
        self.db_cursor.execute('''create table if not exists q_table(state varchar(500), q_value varchar(500))''')
        #data = self.db_cursor.fetchone()
        #print("Connection established to: ",data)
    

    def returnCursor(self):
        cursor= self.db_cursor
        return cursor

    def addDataToDb(self, curr_state, q_value, table):
        db_cursor=self.db_cursor
        selectQuery = 'Select count(*) from '+table +' where state = %s;'
        db_cursor.execute(selectQuery,[curr_state])
        isStateInDb = str(db_cursor.fetchone())
        updateQuery = 'update '+table+' set q_value = %s where state = %s; '
        insertQuery = 'Insert into '+table+'(state,q_value) values(%s,%s); '
        if isStateInDb != '(0,)':
            db_cursor.execute(updateQuery,[q_value,curr_state])
        
        else:
            db_cursor.execute(insertQuery,[curr_state,q_value])

    def fetchData(self, table):
        db_cursor=self.db_cursor
        selectQuery = 'Select * from '+ table+';'
        db_cursor.execute(selectQuery)
        results = db_cursor.fetchall()
        row_dict = {}

        for row in results:
            row_dict[str(row[0])] = float(row[1])
            #print(str(row[0])+":"+float(row[1]))
        return row_dict


    def dbCommit(self):
        self.db_conn.commit()
        

        
