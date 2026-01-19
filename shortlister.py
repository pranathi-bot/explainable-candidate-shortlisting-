import csv
def calculation_score(candidate):
    score=0
    cgpa=float(candidate['CGPA'])
    score+=(cgpa/10)*30

    coding=int(candidate['CodingScore'])
    score+=(coding/100)*40
     
    projects=int(candidate['Projects'])
    score+=min(projects*5,20)

    preferred_skills=['python','DSA']
    skills=candidate['Skills'].split('|')
    skill_score=0
    for skill in skills:
        if skill in preferred_skills:
            skill_score+=5
    score+=min(skill_score,10)
    return round(score,2)



def classify_candidate(score):
    if score >= 75:
        return "Shortlisted"
    elif score>=60:
        return "Borderline"
    else:
        return "Rejected"
    


def explain_decision(candidate):
    reasons=[ ]
    if float(candidate['CGPA'])<7:
        reasons.append("Below-average CGPA")
    if int(candidate['CodingScore'])<60:
        reasons.append("Low Coding score")
    if int(candidate['Projects'])<2:
        reasons.append("Limited project experience")
    if not reasons:
        reasons.append("Strong overall profile")
    return reasons


def bias_check(candidate):
    original_score=calculation_score(candidate)
    adjusted_score=((float(candidate['CGPA'])/10)*20+(int(candidate['CodingScore'])/100)*50+min(int(candidate['Projects'])*5,20))
    return round(original_score,2),round(adjusted_score,2)

def show_all_candidates(candidates):
    for c in candidates:
        print("\nCandidate:",c['Name'])
        print("Score:",c['FinalScore'])
        print("Decision:",c['Decision'])
        print("Reasons:")
        for r in c['Explainations']:
            print("-",r)
        print("Bias Analysis:",c['BiasCheck'])


def show_shortlisted(candidates):
    found=False
    for c in candidates:
        if c['Decision']=="Shortlisted":
            found=True
            print("\Candidate:",c['Name'])
            print("Score:",c['FinalScore'])
        if not found:
            print("\nNo Shortlisted Candidates Found")


def score_visualization(candidates):
    print("\nScore Visualization")
    print("-"*30)
    for c in candidates:
        bars=int(c['FinalScore']//2)
        print(f"{c['Name']}:{''*bars}({c['FinalScore']})")





candidates=[]
with open('candidates.csv','r') as file:
    reader=csv.DictReader(file)
    for row in reader:
        score=calculation_score(row)
        decision=classify_candidate(score)
        explanation=explain_decision(row)
        original,adjusted=bias_check(row)
        original,adjusted=bias_check(row)
        row['FinalScore']=score
        row['Decision']=decision
        row['Explanation']=explanation
        row['BiasCheck']="Stable" if abs(original-adjusted)<5 else "Sensitive"
        candidates.append(row)



print("\n FINAL SHORTLISTING REPORT")
print("-"*40)
for c in candidates:
    print(f"\nCandidate:{c['Name']}")
    print(f"Score:{c['FinalScore']}")
    print(f"Decision:{c['Decision']}")
    print("Reasons:")
    for r in c['Explanation']:
        print("-",r)
    print("Bias Analysis:",c['BiasCheck'])



while True:
    print("\MENU")
    print("1.show all candidates")
    print("2.show shortlisted candidates")
    print("3.Exit")
    print("4.View score visualization")
    choice=input("enter your choice:")
    if choice=='1':
        show_shortlisted(candidates)
    elif choice=='2':
        show_shortlisted(candidates)
    elif choice=='3':
        print("Existing...")
        break
    elif choice=='4':
        score_visualization(candidates)
    else:
        print("Invalid choice")