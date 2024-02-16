import requests
from bs4 import BeautifulSoup

def authenticate_github(client_id, client_secret):
    # Authenticating with GitHub using OAuth app credentials
    auth_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&scope=repo"
    print("Authenticate with GitHub by visiting the following URL and get the authorization code:")
    print(auth_url)
    authorization_code = input("Enter the authorization code: ")

    # Obtaining access token
    token_url = "https://github.com/login/oauth/access_token"
    response = requests.post(token_url, json={"client_id": client_id, "client_secret": client_secret, "code": authorization_code})
    access_token = response.json()["access_token"]
    return access_token

def get_repositories(access_token):
    # Getting all repositories from GitHub
    headers = {"Authorization": f"token {access_token}"}
    repositories_url = "https://api.github.com/user/repos"
    response = requests.get(repositories_url, headers=headers)
    repositories = response.json()
    return repositories

def get_pom_dependencies(repo_url):
    # Parsing Pom.xml file to extract dependencies and versions
    response = requests.get(repo_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dependencies = soup.find_all("dependency")
    for dependency in dependencies:
        group_id = dependency.find("groupId").text
        artifact_id = dependency.find("artifactId").text
        version = dependency.find("version").text
        print(f"{group_id}:{artifact_id} - Version {version}")

def main():
    # Step 1: Authenticate with GitHub
    client_id = input("Enter your GitHub OAuth app client ID: ")
    client_secret = input("Enter your GitHub OAuth app client secret: ")
    access_token = authenticate_github(client_id, client_secret)
    
    # Step 2: Get all repositories
    repositories = get_repositories(access_token)

    # Step 3: Select one repository
    for repo in repositories:
        print(repo['full_name'])

    selected_repo = input("Enter the full name of the repository you want to analyze (e.g., owner/repository_name): ")

    # Step 4: Retrieve Pom.xml files
    repo_url = f"https://github.com/{selected_repo}"
    get_pom_dependencies(repo_url)

if __name__ == "__main__":
    main()
