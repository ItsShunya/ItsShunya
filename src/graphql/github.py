from typing import List, Dict, Tuple, Union
import hashlib
import requests
import os

from cache import cache

HEADERS: Dict[str, str] = {'authorization': 'token ' + os.environ['ACCESS_TOKEN']}
USER_NAME: str = os.environ['USER_NAME']
OUTPUT_PATH: str = "output/"
QUERY_COUNT: Dict[str, int] = {'user_getter': 0, 'follower_getter': 0, 'graph_repos_stars': 0, 'recursive_loc': 0, 'graph_commits': 0, 'loc_query': 0}

def get_query_count():
    return QUERY_COUNT

def query_count(funct_id):
    """
    Counts how many times the GitHub GraphQL API is called
    """
    global QUERY_COUNT
    QUERY_COUNT[funct_id] += 1
    
def force_close_file(data, cache_comment):
    """
    Forces the file to close, preserving whatever data was written to it
    This is needed because if this function is called, the program would've crashed before the file is properly saved and closed
    """
    filename = 'cache/'+hashlib.sha256(USER_NAME.encode('utf-8')).hexdigest()+'.txt'
    with open(filename, 'w') as f:
        f.writelines(cache_comment)
        f.writelines(data)
    print('There was an error while writing to the cache file. The file,', filename, 'has had the partial data saved and closed.')

def simple_request(func_name: str, query: str, variables: Dict[str, Union[str, None]]) -> requests.Response:
    """
    Sends a GraphQL request and returns the response. Raises an exception if it fails.
    """
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=HEADERS)
    if request.status_code == 200:
        return request
    raise Exception(func_name, ' has failed with a', request.status_code, request.text, QUERY_COUNT)

def graph_commits(start_date: str, end_date: str) -> int:
    """
    Returns the total commit count for the specified date range.
    """
    query_count('graph_commits')
    query = '''
    query($start_date: DateTime!, $end_date: DateTime!, $login: String!) {
        user(login: $login) {
            contributionsCollection(from: $start_date, to: $end_date) {
                contributionCalendar {
                    totalContributions
                }
            }
        }
    }'''
    variables = {'start_date': start_date, 'end_date': end_date, 'login': USER_NAME}
    request = simple_request(graph_commits.__name__, query, variables)
    return int(request.json()['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions'])

def graph_repos_stars(
    count_type: str, owner_affiliation: List[str], cursor: Union[str, None] = None, add_loc: int = 0, del_loc: int = 0
) -> Union[int, None]:
    """
    Uses GitHub's GraphQL v4 API to return the total repository count, stars, or LOC count.
    """
    query_count('graph_repos_stars')
    query = '''
    query ($owner_affiliation: [RepositoryAffiliation], $login: String!, $cursor: String) {
        user(login: $login) {
            repositories(first: 100, after: $cursor, ownerAffiliations: $owner_affiliation) {
                totalCount
                edges {
                    node {
                        ... on Repository {
                            nameWithOwner
                            stargazers {
                                totalCount
                            }
                        }
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }'''
    variables = {'owner_affiliation': owner_affiliation, 'login': USER_NAME, 'cursor': cursor}
    request = simple_request(graph_repos_stars.__name__, query, variables)
    if request.status_code == 200:
        if count_type == 'repos':
            return request.json()['data']['user']['repositories']['totalCount']
        elif count_type == 'stars':
            return stars_counter(request.json()['data']['user']['repositories']['edges'])
    return None

def recursive_loc(owner, repo_name, data, cache_comment, addition_total=0, deletion_total=0, my_commits=0, cursor=None):
    """
    Uses GitHub's GraphQL v4 API and cursor pagination to fetch 100 commits from a repository at a time
    """
    query_count('recursive_loc')
    query = '''
    query ($repo_name: String!, $owner: String!, $cursor: String) {
        repository(name: $repo_name, owner: $owner) {
            defaultBranchRef {
                target {
                    ... on Commit {
                        history(first: 100, after: $cursor) {
                            totalCount
                            edges {
                                node {
                                    ... on Commit {
                                        committedDate
                                    }
                                    author {
                                        user {
                                            id
                                        }
                                    }
                                    deletions
                                    additions
                                }
                            }
                            pageInfo {
                                endCursor
                                hasNextPage
                            }
                        }
                    }
                }
            }
        }
    }'''
    variables = {'repo_name': repo_name, 'owner': owner, 'cursor': cursor}
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables':variables}, headers=HEADERS) # I cannot use simple_request(), because I want to save the file before raising Exception
    if request.status_code == 200:
        if request.json()['data']['repository']['defaultBranchRef'] != None: # Only count commits if repo isn't empty
            return loc_counter_one_repo(owner, repo_name, data, cache_comment, request.json()['data']['repository']['defaultBranchRef']['target']['history'], addition_total, deletion_total, my_commits)
        else: return 0
    force_close_file(data, cache_comment) # saves what is currently in the file before this program crashes
    if request.status_code == 403:
        raise Exception('Too many requests in a short amount of time!\nYou\'ve hit the non-documented anti-abuse limit!')
    raise Exception('recursive_loc() has failed with a', request.status_code, request.text, QUERY_COUNT)


def loc_counter_one_repo(owner, repo_name, data, cache_comment, history, addition_total, deletion_total, my_commits):
    """
    Recursively call recursive_loc (since GraphQL can only search 100 commits at a time) 
    only adds the LOC value of commits authored by me
    """
    for node in history['edges']:
        if node['node']['author']['user'] == OWNER_ID:
            my_commits += 1
            addition_total += node['node']['additions']
            deletion_total += node['node']['deletions']

    if history['edges'] == [] or not history['pageInfo']['hasNextPage']:
        return addition_total, deletion_total, my_commits
    else: return recursive_loc(owner, repo_name, data, cache_comment, addition_total, deletion_total, my_commits, history['pageInfo']['endCursor'])

def loc_query(owner_affiliation, comment_size=0, force_cache=False, cursor=None, edges=[]):
    """
    Uses GitHub's GraphQL v4 API to query all the repositories I have access to (with respect to owner_affiliation)
    Queries 60 repos at a time, because larger queries give a 502 timeout error and smaller queries send too many
    requests and also give a 502 error.
    Returns the total number of lines of code in all repositories
    """
    query_count('loc_query')
    query = '''
    query ($owner_affiliation: [RepositoryAffiliation], $login: String!, $cursor: String) {
        user(login: $login) {
            repositories(first: 60, after: $cursor, ownerAffiliations: $owner_affiliation) {
            edges {
                node {
                    ... on Repository {
                        nameWithOwner
                        defaultBranchRef {
                            target {
                                ... on Commit {
                                    history {
                                        totalCount
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }'''
    variables = {'owner_affiliation': owner_affiliation, 'login': USER_NAME, 'cursor': cursor}
    request = simple_request(loc_query.__name__, query, variables)
    if request.json()['data']['user']['repositories']['pageInfo']['hasNextPage']:   # If repository data has another page
        edges += request.json()['data']['user']['repositories']['edges']            # Add on to the LoC count
        return loc_query(owner_affiliation, comment_size, force_cache, request.json()['data']['user']['repositories']['pageInfo']['endCursor'], edges)
    else:
        return cache.cache_builder(edges + request.json()['data']['user']['repositories']['edges'], comment_size, force_cache)

def add_archive():
    """
    Several repositories I have contributed to have since been deleted.
    This function adds them using their last known data
    """
    with open('cache/repository_archive.txt', 'r') as f:
        data = f.readlines()
    old_data = data
    data = data[7:len(data)-3] # remove the comment block    
    added_loc, deleted_loc, added_commits = 0, 0, 0
    contributed_repos = len(data)
    for line in data:
        repo_hash, total_commits, my_commits, *loc = line.split()
        added_loc += int(loc[0])
        deleted_loc += int(loc[1])
        if (my_commits.isdigit()): added_commits += int(my_commits)
    added_commits += int(old_data[-1].split()[4][:-1])
    return [added_loc, deleted_loc, added_loc - deleted_loc, added_commits, contributed_repos]

def stars_counter(data):
    """
    Count total stars in repositories owned by me
    """
    total_stars = 0
    for node in data: total_stars += node['node']['stargazers']['totalCount']
    return total_stars

def commit_counter(comment_size):
    """
    Counts up my total commits, using the cache file created by cache_builder.
    """
    total_commits = 0
    filename = 'cache/'+hashlib.sha256(USER_NAME.encode('utf-8')).hexdigest()+'.txt' # Use the same filename as cache_builder
    with open(filename, 'r') as f:
        data = f.readlines()
    cache_comment = data[:comment_size] # save the comment block
    data = data[comment_size:] # remove those lines
    for line in data:
        total_commits += int(line.split()[2])
    return total_commits

def user_getter(username):
    """
    Returns the account ID and creation time of the user
    """
    query_count('user_getter')
    query = '''
    query($login: String!){
        user(login: $login) {
            id
            createdAt
        }
    }'''
    variables = {'login': username}
    request = simple_request(user_getter.__name__, query, variables)
    return {'id': request.json()['data']['user']['id']}, request.json()['data']['user']['createdAt']

def follower_getter(username):
    """
    Returns the number of followers of the user
    """
    query_count('follower_getter')
    query = '''
    query($login: String!){
        user(login: $login) {
            followers {
                totalCount
            }
        }
    }'''
    request = simple_request(follower_getter.__name__, query, {'login': username})
    return int(request.json()['data']['user']['followers']['totalCount'])