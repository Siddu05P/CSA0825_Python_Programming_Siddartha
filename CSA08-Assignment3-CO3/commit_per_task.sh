#!/bin/sh
# One commit per task, as the assignment requires. Run once inside this folder after installing git.
git init
git add README.md .gitignore && git commit -m "Add README"
git add q1_rainfall_lists && git commit -m "Add q1_rainfall_lists: program, output and screenshots"
git add q2_tuples_copying && git commit -m "Add q2_tuples_copying: program, output and screenshots"
git add q3_dictionaries && git commit -m "Add q3_dictionaries: program, output and screenshots"
git add q4_sets && git commit -m "Add q4_sets: program, output and screenshots"
git add q5_comprehensions && git commit -m "Add q5_comprehensions: program, output and screenshots"
git add q6_railway_nested && git commit -m "Add q6_railway_nested: program, output and screenshots"
git add q7_contact_merging && git commit -m "Add q7_contact_merging: program, output and screenshots"
echo "Now: git branch -M main; git remote add origin <your GitHub URL>; git push -u origin main"
