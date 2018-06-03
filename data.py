import sqlite3
import os

def _readsql():
    execdir = os.path.dirname(os.path.realpath(__file__))
    sqlpath = os.path.join(execdir, 'sql')
    sqldirs = [name for name in os.listdir(sqlpath)
               if os.path.isdir(os.path.join(sqlpath, name))]

    sql = dict()
    for dirname in sqldirs:
        sql[dirname] = dict()
        sqlfiles = [name for name in os.listdir(os.path.join(sqlpath, dirname))
                    if name.endswith('.sql')]
        for fname in sqlfiles:
            with open(os.path.join(sqlpath, dirname, fname)) as fh:
                sql[dirname][os.path.splitext(fname)[0]] = fh.read()
    return sql
_sql = _readsql()

class Database():
    def __init__(self, dbname, maxuncommited=25):
        self._dbname = dbname
        self._maxuncommited = maxuncommited
    def __enter__(self):
        self.open()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def open(self):
        self._conn = sqlite3.connect(self._dbname)
    def close(self):
        self._conn.commit()
        self._conn.close()
    
    def getexercise(self, name, cursor=None):
        no_cursor = cursor is None
        if no_cursor: cursor = self._conn.cursor()
        params = { \
            'name': name, \
        }
        cursor.execute(_sql['exercises']['read_by_name'], params)
        row = cursor.fetchall()[0]

        return { 'id': row[0], 'name': row[1], 'type': row[2] }

    def addmovement(self, date, time, ex_id, ex_name, ex_type, comment, cursor=None):
        no_cursor = cursor is None
        if no_cursor: cursor = self._conn.cursor()
        params = { \
            'date': date, \
            'time': time, \
            'exercise_id': ex_id, \
            'exercise': ex_name, \
            'type': ex_type, \
            'comment': comment, \
        }
        cursor.execute(_sql['workouts']['insert_one'], params)
        rowid = cursor.lastrowid
        if no_cursor: cursor.close()
        return rowid
    
    def addset(self, movement_id, weight, rep, cursor=None):
        no_cursor = cursor is None
        if no_cursor: cursor = self._conn.cursor()
        params = { \
            'date_id': movement_id, \
            'weight': weight, \
            'rep': rep, \
        }
        cursor.execute(_sql['reps']['insert_one'], params)
        rowid = cursor.lastrowid
        if no_cursor: cursor.close()
        return rowid

    def loadworkouts(self, workouts):
        exercisecache = dict()
        cursor = self._conn.cursor()

        for (date, movements) in workouts.items():
            for movement in movements:
                # retrieve exercise
                exercise = None
                if movement['name'] in exercisecache:
                    exercise = exercisecache[movement['name']]
                else:
                    exercise = self.getexercise(movement['name'])
                    exercisecache[exercise['name']] = exercise
                # add workout
                workout_id = self.addmovement(date, '00:00', exercise['id'], exercise['name'], exercise['type'], '', cursor)

                for rep in movement['reps']:
                    # add rep (rep_id, workout_id, float(rep[0]), rep[1])
                    self.addset(workout_id, rep[1], rep[0], cursor)

        cursor.close()

