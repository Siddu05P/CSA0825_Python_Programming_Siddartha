#!/bin/sh
# One commit per task, as the assignment requires. Run once inside this folder after installing git.
git init
git add README.md .gitignore && git commit -m "Add README"
git add b1_cleaning_storage_charts && git commit -m "Add b1_cleaning_storage_charts: program, output and screenshots"
git add b2_adversarial_data && git commit -m "Add b2_adversarial_data: program, output and screenshots"
git add b3_loops_vs_libraries_vs_sql && git commit -m "Add b3_loops_vs_libraries_vs_sql: program, output and screenshots"
git add b4_final_decision && git commit -m "Add b4_final_decision: program, output and screenshots"
echo "Now: git branch -M main; git remote add origin <your GitHub URL>; git push -u origin main"
