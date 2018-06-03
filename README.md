My Nexus 5X died a horrible, fiery (bootloop-ing) death, and it took several years of workout data with it. Those workouts had been stored locally inside the [Simple Workout Log](https://play.google.com/store/apps/details?id=com.selahsoft.workoutlog) app.

Fortunately, I simultaneously logged workouts in the [StrongLifts 5x5](https://play.google.com/store/apps/details?id=com.stronglifts.app) app which has a paid option for history export (among other things).

I put this script together to allow me to copy my old workouts from StrongLifts 5x5 to Simple Workout Log. To run it:

~~~bash
$ python ./runimport.py ./workouts.xlsx
~~~

If you've changed the name of the default workoutlogs db file from `workoutlog.bak`, you'll need to include a `--sqlite_file $DBFILENAME` argument.

Expected data format can be viewed in the provided `workouts.xlsx` file.
