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
        self.data = self.db_cursor.fetchone()
        print("Connection established to: ",self.data)

    def addDataToDb(self, curr_state, q_value):
        print("adding values to db ", curr_state, q_value)
        self.db_cursor.execute('''Insert into q_table(state,q_value) values(%s,%s)''',(curr_state,q_value));

    def dbCommit(self):
        self.db_conn.commit()
        

        
