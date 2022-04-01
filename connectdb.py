import psycopg2
import os
import globalvar

def getConnection():
  dict_connection = dict()
  port = globalvar.port
  db = globalvar.db
  user = globalvar.user
  pswd = globalvar.pswd
  if os.environ.get('GAE_ENV') == 'standard':
    host = '/cloudsql/%s' % (globalvar.instance_name)
  else:
    host = '127.0.0.1'
  string_params = (host, port, db, user, pswd)
  dict_connection['ksb-2022'] = """
    host='%s' port=%s dbname='%s' user='%s' password='%s'
    """ % string_params

  return dict_connection

class Database() :
  def __init__(self, param, autocommit=True):
    self._dict_connection = getConnection()
    self._connection_det = self._dict_connection.get(param)
    self.autocommit = autocommit
    try:
      self._conn = psycopg2.connect(self._connection_det)
      self._curs = self._conn.cursor()
      self._curs.execute("SET TIMEZONE='Asia/Jakarta'")
    except psycopg2.Error as error:
      raise Exception('%s, Database : %s' % (error, 'Tidak Ditemukan'))

  def select(self, text_query):
    '''
      Fungsi ini digunakan untuk select query tanpa parameter
      @param select_string: Merupakan statement query yang dipakai
    '''
    status = False
    try:
      self._curs.execute(text_query)
      data = self._curs.fetchall()
      status = True
    except psycopg2.Error as error:
      data = "Error {} - {}".format(text_query, error)
    result = data
    return status, result

  def execute(self, text_query, value):
    '''
      Fungsi ini digunakan untuk insert,update,delete query dengan parameter value
    '''
    status = False
    try:
      self._curs.execute(text_query,value)
      self._conn.commit()
      data = self._curs.rowcount
      status = True
    except psycopg2.Error as error:
      data = "Error {} - {}".format(text_query,error)
    result = str(data) + " row executed"
    return status, result


