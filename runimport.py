from argparse import ArgumentParser
from extract import Extract
from data import Database

parser = ArgumentParser(description='Import old workouts to workoutlog.bak sqlite file.')

parser.add_argument('spreadsheet',
                    help='Spreadsheet with old workouts to import.')

parser.add_argument('--sqlite_file',
                    help='Sqlite file to import old workouts into.',
                    default='./workoutlog.bak')

args = parser.parse_args()

oldworkouts = Extract.getoldworkouts(args.spreadsheet)

with Database(args.sqlite_file) as db:
    db.loadworkouts(oldworkouts)
