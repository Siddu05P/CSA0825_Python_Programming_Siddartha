#!/bin/sh
# One commit per task, as the assignment requires. Run once inside this folder after installing git.
git init
git add README.md .gitignore && git commit -m "Add README"
git add task1_mess_bills && git commit -m "Add task1_mess_bills: program, output and screenshots"
git add task2_attendance_files && git commit -m "Add task2_attendance_files: program, output and screenshots"
git add task3_exceptions && git commit -m "Add task3_exceptions: program, output and screenshots"
git add task4_file_forensics && git commit -m "Add task4_file_forensics: program, output and screenshots"
git add task5_four_organisations && git commit -m "Add task5_four_organisations: program, output and screenshots"
git add task6_fest_registration && git commit -m "Add task6_fest_registration: program, output and screenshots"
echo "Now: git branch -M main; git remote add origin <your GitHub URL>; git push -u origin main"
