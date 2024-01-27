Noah Fuery
1/26/2024
CPSC 406 - Algorithm Analysis
Dr. Erik Linstead

How to run program on command lin:
python3 NFAtoDFA.py "Name of input file"

Difficulties and Successes:
I managed to get most of the logic complete for the transitions and reading and writing the files. I struggled a lot with the dfa transitions as I realized way too late that my nfa transitions were not all being stored as I was using a dictionary to store them, so each key was storing only one value. If I had more time I would fix this. I also had trouble finding the accept states due to the fact that they are dependent on the transitions being done. Another problem I spent a long time on was handling multiple transition options for each state, i.e. if state {2} could go to either itself with a or {3} with a. 

Sources:
https://www.geeksforgeeks.org/command-line-interface-programming-python/
https://stackoverflow.com/questions/11178061/print-list-without-brackets-in-a-single-row