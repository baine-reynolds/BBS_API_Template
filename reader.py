import requests
import getpass
import json


#####  Init
def parse_args():
    parser = OptionParser()
    parser.add_option('-t', '--use-token', action='count', dest='token', default=0, help="Use API token instead of username/password")
    options, args = parser.parse_args()
    return options, args

def get_creds(options):
    session = requests.Session()
    base_url = input("Please enter the Source instance's Base URL (i.e. https://bitbucket.mycompany.com (Server)):\n")
    if options.token == 0: # standard auth
        admin_user = input("Please enter the Admin username for your source environment:\n")
        admin_password = getpass.getpass("Please enter the Admin password for your source environment:\n")
        session.auth = (admin_user, admin_password)
    else: # token auth
        token = input("Please enter your auth token.\n")
        session.headers = {'Authorization': "Basic " + token}
    return base_url, session


##### Run Operations
def projects(base_url, session, paged_start=None, paged_limit=None):
    while True:
        params = {'start': paged_start, 'limit': paged_limit}
        try:
            r = session.get(f"{base_url}/rest/api/1.0/projects/", params=params)
        except requests.exceptions.SSLError:
            r = session.get(f"{base_url}/rest/api/1.0/projects/", params=params verify=False)

        r_data = r.json()
        for project_json in r_data['values']:
            yield project_json
        if r_data['isLastPage'] == True:
            return
        paged_start = r_data['nextPageStart']

def repos(base_url, session, project, paged_start=None, paged_limit=None):
    while True:
        params = {'start': paged_start, 'limit': paged_limit}
        try:
            r = session.get(f"{base_url}/rest/api/1.0/projects/{project['key']}/repos/", params=params)
        except requests.exceptions.SSLError:
            r = session.get(f"{base_url}/rest/api/1.0/projects/{project['key']}/repos/", params=params verify=False)

        r_data = r.json()
        for project_json in r_data['values']:
            yield project_json
        if r_data['isLastPage'] == True:
            return
        paged_start = r_data['nextPageStart']

##### Start
def main():
    options, args = parse_args()
    base_url, session = get_creds(options)

    for project in projects(base_url, session):
        # Action on projects
        # print(project['key'])
        # print(project)
        for repo in repos(base_url, session, project):
            # Action on repos
            # print(repo['slug'])
            # print(repo)


if __name__ == '__main__':
    main()