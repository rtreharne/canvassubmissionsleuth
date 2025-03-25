import pandas as pd
from canvasapi import Canvas
from getpass import getpass

def create_canvas_session(API_URL, API_TOKEN):
    # Prompt for API credentials if not provided
    if not API_URL or not API_TOKEN:    
        API_URL = input("Please input your Canvas URL, e.g. 'https://canvas.liverpool.ac.uk': ")
        API_TOKEN = getpass("Please input your API token: ") 
    
    # Create and return a Canvas API session
    canvas = Canvas(API_URL, API_TOKEN) 
    return canvas 

def get_submissions(assignment):
    submissions = [x for x in assignment.get_submissions(include=['user', 'submission_comments'])]
    return submissions

def get_graders_from_ids(canvas, ids):
    graders = {}
    for id in ids:
        try:
            graders[id] = canvas.get_user(id).sortable_name
        except:
            graders[id] = None
    return graders

def clean_data(submission):
    cleaned_sub = {}
    
    for key in submission.__dict__.keys():
        # Ignore keys with dictionary values
        #print(key)
        if not isinstance(submission.__dict__[key], (dict, list) ):
            cleaned_sub[key] = submission.__dict__[key]

        elif key == 'user':

            cleaned_sub[key] = submission.__dict__[key]['sortable_name']
            

        elif key == 'submission_comments':
 
            commenters = []
            for comment in submission.__dict__[key]:
                commenters.append(comment['id'])
            cleaned_sub['commenter_ids'] = commenters
    
    return cleaned_sub

def main(API_URL=None, API_TOKEN=None):

    print("""
::::::::::: :::::::::: :::              ::::::::   ::::::::  :::::::::   ::::::::  
    :+:     :+:        :+:             :+:    :+: :+:    :+: :+:    :+: :+:    :+: 
    +:+     +:+        +:+             +:+        +:+    +:+ +:+    +:+ +:+        
    +#+     +#++:++#   +#+             +#++:++#++ +#+    +:+ +#++:++#+  +#++:++#++ 
    +#+     +#+        +#+                    +#+ +#+    +#+ +#+    +#+        +#+ 
    #+#     #+#        #+#             #+#    #+# #+#    #+# #+#    #+# #+#    #+# 
    ###     ########## ##########       ########   ########  #########   ########  
    """)
    print("")
    print("TEL Team, School of Biosciences, University of Liverpool. 2025")
    print("")
    
    canvas = create_canvas_session(API_URL, API_TOKEN) 

    course_id = input("Please input the course ID: ")
    assignment_id = input("Please input the assignment ID: ")

    print("Fetching data...")

    submissions = get_submissions(canvas.get_course(course_id).get_assignment(assignment_id))

    print("Cleaning data...")

    # Clean the data
    cleaned_data = [clean_data(x) for x in submissions]

    print("Fetching grader information...")

    # Create a pandas DataFrame
    df = pd.DataFrame(cleaned_data)

    grader_ids = df["grader_id"].tolist()
    graders = get_graders_from_ids(canvas, set(grader_ids))
    df["grader_name"] = [graders[x] for x in grader_ids]

    # Flatten commenter_ids to a list of unique IDs
    commenter_ids_flat = set([id for sublist in df["commenter_ids"].tolist() for id in sublist])

    # Find IDs that are not already in the graders dict
    missing_ids = commenter_ids_flat - set(graders.keys())

    # If there are missing IDs, use get_graders_from_ids to fetch the corresponding grader info
    if missing_ids:
        new_graders = get_graders_from_ids(canvas, missing_ids)
        
        # Merge the new grader information with the existing graders dict
        graders.update(new_graders)
    
    df["commenter_names"] = [[graders[x] for x in ids] for ids in df["commenter_ids"]]

    # sort order of columns by alphabetically
    df = df.reindex(sorted(df.columns), axis=1)

    fname = f"{course_id}_{assignment_id}.csv"
    print(f"Saving data to {fname}...")

    df.to_csv(f"{course_id}_{assignment_id}.csv", index=False)

    print("Done!")

if __name__ == "__main__":
    # Import API credentials from a config file
    from config import API_URL, API_TOKEN
    
    # Run the script
    main(API_URL, API_TOKEN)