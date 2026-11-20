#!/bin/sh
# One commit per task, as the assignment requires. Run once inside this folder after installing git.
git init
git add README.md .gitignore && git commit -m "Add README"
git add q1_subsidy && git commit -m "Add q1_subsidy: program, output and screenshots"
git add q2_otp_loops && git commit -m "Add q2_otp_loops: program, output and screenshots"
git add q3_vehicle_numbers && git commit -m "Add q3_vehicle_numbers: program, output and screenshots"
git add q4_string_building && git commit -m "Add q4_string_building: program, output and screenshots"
git add q5_functions_scope && git commit -m "Add q5_functions_scope: program, output and screenshots"
git add q6_recursion && git commit -m "Add q6_recursion: program, output and screenshots"
git add q7_redesign && git commit -m "Add q7_redesign: program, output and screenshots"
echo "Now: git branch -M main; git remote add origin <your GitHub URL>; git push -u origin main"
