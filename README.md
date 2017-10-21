# networks_ass2
## Run base assignment
- Use packet rate of 1
- SHP:
```
python -m routing_performance CIRCUIT SHP topology.txt workload.txt 1
```
- SDP:
```
python -m routing_performance CIRCUIT SDP topology.txt workload.txt 1
```
- LLP (broken atm):
```
python -m routing_performance CIRCUIT LLP topology.txt workload.txt 1
```
- Debug:
```
python -m pdb routing_performance.py CIRCUIT SDP topology.txt workload.txt 1
```


## Git commands 
- Clone specific branch
```
git clone -b master https://github.com/AlexN34/networks_ass2.git
```
- Create new branch and push it on server side
```
git branch new_branch_name
git checkout new_branch_name
git push --set-upstream origin new_branch_name
```
- Merge changes from branch with another branch 
```
git checkout master
git pull origin other_branch_name
# alternatively, can use merge instead i think?
git push

```
- Shit, need to go back in time
```
git log
# pick commit hash number
git checkout hash_number
# you're now in detached head state, do below when you want to go back
git checkout ^HEAD
# ^ that's from memory, may or may not work lol
```
# Structure
- djikstra folder to be added for naive algo implementation
- ds for datastructures and graphrep
- report for documentation type stuff for submission
