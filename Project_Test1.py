from candidate_loader import load_candidates

#Loads the candidates(file_name,limit)
 
for candidate in load_candidates("candidates.jsonl", limit=1):
    print(candidate["profile"])

    
    