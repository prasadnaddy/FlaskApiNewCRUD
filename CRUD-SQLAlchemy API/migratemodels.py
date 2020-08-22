Steps to be followed to run the next scripts for migration##
1. py <MigrationScript.py> db init --> To initiate the database or else create one if not exists
2. We get a new migrations folder, and inside that we get a file named "alembic.ini" we need to configure it if required
3. Next run this command for the migration process, py <MigrationScript.py> db migrate -m "Message of change"
4. Now we observe that a new script file is created that is going to do the changes, refer it in /migrations/versions/
5. We get two definiations, inside it named upgrade() and downgrade(), upgrade adds the changes and downgrade removes the tables
6. Now if we type py <Migratescript.py> db upgrade to run the new columns/ models to be added to the Database
7. Now we will remove the new column inside the model named Pet, and then use migrate command to get a new script in /migrations/versions/
8. Now we see that upgrade() function will remove the new column and downgrade() function will restore the new column, choice is yours.
9. Type the upgrade command to make the changes in the database.