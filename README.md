# smashstats


A global and regional ranking system and tournament database for competitive Super Smash Bros Melee.

Setting up a local SmashStats server and database

## WORKING ENVIRONMENT
0. Clone matchstats repo
1. Download Python 2.7
2. sudo easy_install virtualenv
3. virtualenv flask
4. Activate virtualenv: `. flask/bin/activate[.yourshell]`
5. Install pip: `install pip`
6. Install requirements: `pip install -r requirements.txt`
7. install pychallonge: `pip install -e git+http://github.com/russ-/pychallonge#egg=pychallonge`
8. pip install iso8601

## DATABASE CONFIG
If you cloned the git repo correctly, you should have a populated and working SQLite database.

1. First, test the Shell. This command loads a python shell for testing with automatically imported environment modules. You should see a message "Imported modules for SmashStats"
`$ python -i startup.py`

2. Test to see if the database is populated by running simple SQLAlchemy commands like

```python
len(User.query.all()) #returns length of list of all Users in database
Region.query.all() #returns list of all Regions in database
```

3. If some SQL error is thrown, the database isn't populated yet. Otherwise, skip to the next section
4. Exit the shell, and delete the current SQLite database.

`$ rm app2.db`

5. Create the database, migrate, and upgrade it using 3 scripts sequentially

```bash
$ ./db_create.py
$ ./db_migrate.py
$ ./db_upgrade.py
```

6. If no errors are thrown, you should be good to go. Now populate your database by running these 2 scripts:

```bash
$ ./database_maintenance/character_create.py
$ ./database_maintenance/region_create.py
```

7. At this point you have a working, but empty database.

## RUNNING THE SERVER
1. Simply run this command:
$ ./run.py

Then navigate to http://localhost:5000 or wherever the address to your local server is. If your database is unpopulated, no data will appear. If your database is not setup correctly, you will actually run into some error within viewing a few pages. If the database is populated, you should be able to navigate around your local site as if it were the live version of SmashStats.

## DATABASE MAINTENANCE
Now that you have a working database, it's up to you what you want to do with it.

1. If you want to clear the database of its contents then add your own, run this command:
`$ ./database_maintenance/clear_database.py`

2. If you would like to add a new Region, in the shell run this command:
`add_region("your_region_name")``

Now you can try adding new tournaments if you wish.
3. Enter the folder containing tournament lists to process
`$ cd tournamentlists`

4. Open one of these .txt files up and understand the format in which tournaments are uploaded in
5. Make a new .txt file in this directory, and name it whatever you'd like. Then add the tournaments you wish to upload, one tournament per line
6. After you have saved your .txt file, you can exit and return to the root directory. Then process the tournamentlists like so:

`$ ./process_tournamentlist.py tournamentlists/[tournamentlist.txt] ["Region"]`

Replace `tournamentlist.txt` with the name of the .txt file you created, and replace `"Region"` with a string of the region the tournaments came from. If you just want everything as the global region, put None here. This function may take a while to run, depending on the length of the tournamentlist

7. You can view your updated database by simply running the server: `$ ./run.py`
8. Likely there are some things to manually fix, such as merging two Users. Open up the file `database_maintenance/NE_database_maintenance.py` and see what kinds of maintenance functions you can use. Open up `maintenance_utils.py` for even more information about maintenance functions.
10. You can duplicate this script or make a new one entirely. I highly recommend including these commands at the top of your script regardless of what data is actually in your database:

```python
remove_team('|') # Clears sponsor information by recognizing a specific character
capitalize_all_tags() # capitalizes all tags and standardizes your database
```

11. Once you've inputted whatever maintenance functions you wish to do, simply run the script from the root directory:
`$ ./database_maintenance/[my_db_maintenance.py]`

You don't need to disable any of the maintenance functions once you've used them once. The functions  are intelligent enough that you won't, for example, add a duplicate character for a User.

12. Now that some Users are merged, you've essentially altered the timeline of results. For example, if a duplicate User had sets from 3 months ago, and you merge him with his main profile, essentially the duplicate player never existed and we can't use that duplicate to calculate TrueSkill. So since the TrueSkill algorithm doesn't recalculate automatically, we need to run a script to do that:
`$ ./recalculate_trueskills_dict.py`

This function will "replay" every set in the database in chronological order, and recalculate TrueSkills using this correct timeline of results. It may take quite some time depending on the size of your database and the speed of your CPU.
