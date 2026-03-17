def youtube_resources(skills):

    resources = {}

    for skill in skills:

        resources[skill] = f"https://www.youtube.com/results?search_query={skill}+tutorial"

    return resources