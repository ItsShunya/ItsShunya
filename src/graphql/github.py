# The Python Standard Library.
from typing import List, Dict, Union, Tuple
import hashlib
import requests
import os

# Project's internal modules.
from cache import cache

HEADERS: Dict[str, str] = {'Authorization': 'token ' + os.environ['ACCESS_TOKEN'], 'User-Agent': 'github-profile-stats/1.0'}
USER_NAME: str = os.environ['USER_NAME']
OUTPUT_PATH: str = "output/"
QUERY_COUNT: Dict[str, int] = {'user_getter': 0, 'follower_getter': 0, 'graph_repos_stars': 0, 'recursive_loc': 0, 'graph_commits': 0, 'loc_query': 0}
OWNER_ID: str = ''

REQUEST_TIMEOUT = (5, 30)  # connect, read

def get_query_count():
    """
    Returns the current count of GitHub GraphQL API queries made.

    Returns
    -------
    Dict[str, int]
        Dictionary containing the count of each type of query made.
    """
    return QUERY_COUNT

def set_owner_id(new_OWNER_ID: str):
    """
    Sets the global OWNER_ID variable to the specified user ID.

    Parameters
    ----------
    new_OWNER_ID : str
        The user ID to set as the global OWNER_ID.
    """
    global OWNER_ID
    OWNER_ID = new_OWNER_ID

def query_count(funct_id: str):
    """
    Increments the count of the specified query type in the QUERY_COUNT dictionary.

    Parameters
    ----------
    funct_id : str
        The identifier of the query type to increment.
    """
    global QUERY_COUNT
    QUERY_COUNT[funct_id] += 1

def force_close_file(data: List[str], cache_comment: List[str]):
    """
    Forces the cache file to close, preserving the data written to it.

    This function is used when an error occurs to ensure partial data is saved.

    Parameters
    ----------
    data : List[str]
        The data to write to the file.
    cache_comment : List[str]
        The comment block to prepend to the data.
    """
    filename = 'cache/' + hashlib.sha256(USER_NAME.encode('utf-8')).hexdigest() + '.txt'
    with open(filename, 'w') as f:
        f.writelines(cache_comment)
        f.writelines(data)
    print('There was an error while writing to the cache file. The file,', filename, 'has had the partial data saved and closed.')

def simple_request(func_name: str, query: str, variables: Dict[str, Union[str, None]]) -> requests.Response:
    """
    Sends a GraphQL request to the GitHub API and returns the response.

    Parameters
    ----------
    func_name : str
        The name of the calling function.
    query : str
        The GraphQL query to send.
    variables : Dict[str, Union[str, None]]
        The variables to include with the query.

    Returns
    -------
    requests.Response
        The response from the GitHub API.

    Raises
    ------
    Exception
        If the request fails with a non-200 status code.
    """
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    if request.status_code == 200:
        return request
    raise Exception(func_name, ' has failed with a', request.status_code, request.text, QUERY_COUNT)

def graph_commits(start_date: str, end_date: str) -> int:
    """
    Returns the total commit count for the specified date range.

    Parameters
    ----------
    start_date : str
        The start date of the range in ISO format.
    end_date : str
        The end date of the range in ISO format.

    Returns
    -------
    int
        The total number of commits in the specified date range.
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

    Parameters
    ----------
    count_type : str
        The type of count to perform ('repos', 'stars', or 'loc').
    owner_affiliation : List[str]
        List of repository affiliations to consider.
    cursor : Union[str, None], optional
        Cursor for pagination (default: None).
    add_loc : int, optional
        Lines of code added counter (default: 0).
    del_loc : int, optional
        Lines of code deleted counter (default: 0).

    Returns
    -------
    Union[int, None]
        The total count of repositories, stars, or LOC, or None if the count type is invalid.
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

def recursive_loc(owner: str, repo_name: str, data: List[str], cache_comment: List[str], addition_total: int = 0, deletion_total: int = 0, my_commits: int = 0, cursor: Union[str, None] = None) -> Union[Tuple[int, int, int], None]:
    """
    Uses GitHub's GraphQL v4 API and cursor pagination to fetch 100 commits from a repository at a time.

    Parameters
    ----------
    owner : str
        The owner of the repository.
    repo_name : str
        The name of the repository.
    data : List[str]
        The data being processed.
    cache_comment : List[str]
        The comment block to prepend to the data.
    addition_total : int, optional
        Lines of code added counter (default: 0).
    deletion_total : int, optional
        Lines of code deleted counter (default: 0).
    my_commits : int, optional
        Number of commits authored by the user (default: 0).
    cursor : Union[str, None], optional
        Cursor for pagination (default: None).

    Returns
    -------
    Union[Tuple[int, int, int], None]
        A tuple containing the total additions, deletions, and commits authored by the user, or None if the request fails.
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
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables':variables}, headers=HEADERS, timeout=REQUEST_TIMEOUT) # I cannot use simple_request(), because I want to save the file before raising Exception
    if request.status_code == 200:
        if request.json()['data']['repository']['defaultBranchRef'] != None: # Only count commits if repo isn't empty
            return loc_counter_one_repo(owner, repo_name, data, cache_comment, request.json()['data']['repository']['defaultBranchRef']['target']['history'], addition_total, deletion_total, my_commits)
        else: return 0
    force_close_file(data, cache_comment) # saves what is currently in the file before this program crashes
    if request.status_code == 403:
        raise Exception('Too many requests in a short amount of time!\nYou\'ve hit the non-documented anti-abuse limit!')
    raise Exception('recursive_loc() has failed with a', request.status_code, request.text, QUERY_COUNT)


def loc_counter_one_repo(owner: str, repo_name: str, data: List[str], cache_comment: List[str], history: Dict[str, Union[List[Dict[str, Union[str, int]]], Dict[str, Union[str, bool]]]], addition_total: int, deletion_total: int, my_commits: int) -> Tuple[int, int, int]:
    """
    Recursively calls recursive_loc to fetch commit history and calculate LOC statistics.

    Parameters
    ----------
    owner : str
        The owner of the repository.
    repo_name : str
        The name of the repository.
    data : List[str]
        The data being processed.
    cache_comment : List[str]
        The comment block to prepend to the data.
    history : Dict[str, Union[List[Dict[str, Union[str, int]]], Dict[str, Union[str, bool]]]]
        The commit history data.
    addition_total : int
        Lines of code added counter.
    deletion_total : int
        Lines of code deleted counter.
    my_commits : int
        Number of commits authored by the user.

    Returns
    -------
    Tuple[int, int, int]
        A tuple containing the total additions, deletions, and commits authored by the user.
    """
    for node in history['edges']:
        if node['node']['author']['user'] == OWNER_ID:
            my_commits += 1
            addition_total += node['node']['additions']
            deletion_total += node['node']['deletions']

    if history['edges'] == [] or not history['pageInfo']['hasNextPage']:
        return addition_total, deletion_total, my_commits
    else:
        return recursive_loc(owner, repo_name, data, cache_comment, addition_total, deletion_total, my_commits, history['pageInfo']['endCursor'])

def loc_query(owner_affiliation: List[str], comment_size: int = 0, force_cache: bool = False, cursor: Union[str, None] = None, edges: List = []):
    """
    Uses GitHub's GraphQL v4 API to query all the repositories I have access to (with respect to owner_affiliation)
    Queries 60 repos at a time, because larger queries give a 502 timeout error and smaller queries send too many
    requests and also give a 502 error.
    Returns the total number of lines of code in all repositories

    Parameters
    ----------
    owner_affiliation : List[str]
        List of repository affiliations to consider.
    comment_size : int, optional
        Number of lines to preserve as comments (default: 0).
    force_cache : bool, optional
        Flag to force cache recreation (default: False).
    cursor : Union[str, None], optional
        Cursor for pagination (default: None).
    edges : List, optional
        List of repository edges (default: []).

    Returns
    -------
    Any
        The result of the cache_builder function.
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
    Adds statistics for archived repositories that have been deleted.

    Several repositories I have contributed to have since been deleted.
    This function adds them using their last known data from a cache file.

    Returns
    -------
    list
        A list containing:
        - added_loc : int
            Total lines of code added
        - deleted_loc : int
            Total lines of code deleted
        - net_loc : int
            Net lines of code change (added - deleted)
        - added_commits : int
            Total commits made
        - contributed_repos : int
            Number of repositories contributed to
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
    Counts total stars in repositories owned by the user.

    Parameters
    ----------
    data : list
        List of repository data dictionaries

    Returns
    -------
    int
        Total number of stars across all repositories
    """
    total_stars = 0
    for node in data: total_stars += node['node']['stargazers']['totalCount']
    return total_stars

def commit_counter(comment_size):
    """
    Counts total commits using cached repository data.

    Parameters
    ----------
    comment_size : int
        Number of lines in the comment block of the cache file

    Returns
    -------
    int
        Total number of commits
    """
    total_commits = 0
    filename = 'cache/'+hashlib.sha256(USER_NAME.encode('utf-8')).hexdigest()+'.txt'
    with open(filename, 'r') as f:
        data = f.readlines()
    cache_comment = data[:comment_size]
    data = data[comment_size:]
    for line in data:
        total_commits += int(line.split()[2])
    return total_commits

def user_getter(username):
    """
    Retrieves user account information.

    Parameters
    ----------
    username : str
        GitHub username to query

    Returns
    -------
    tuple
        A tuple containing:
        - dict
            User ID information with keys:
            - id : str
                User's GitHub ID
        - str
            User account creation date

    Raises
    ------
    Exception
        If the GitHub API request fails
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
    Gets the number of followers for a GitHub user.

    Parameters
    ----------
    username : str
        GitHub username to query

    Returns
    -------
    int
        Number of followers

    Raises
    ------
    Exception
        If the GitHub API request fails
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
