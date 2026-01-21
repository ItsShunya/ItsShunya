"""Cache management module for repository data storage and updates."""

import hashlib
import os

from graphql import github
from config.environment import EnvConfig

env = EnvConfig.from_env()
USER_NAME: str = env.USER_NAME


def cache_builder(
    edges: list,
    comment_size: int,
    force_cache: bool,
    loc_add: int = 0,
    loc_del: int = 0,
) -> list[int | bool]:
    """
    Builds or updates the cache file with repository data.

    Parameters
    ----------
    edges : list
        List of repository edges containing node information
    comment_size : int
        Number of lines to preserve as comments
    force_cache : bool
        Flag to force cache recreation
    loc_add : int, optional
        Lines of code added counter (default: 0)
    loc_del : int, optional
        Lines of code deleted counter (default: 0)

    Returns
    -------
    list[int | bool]
        A list containing:
        - Total lines added (int)
        - Total lines deleted (int)
        - Net change (int)
        - Cache status (bool)

    Raises
    ------
    IOError
        If there is an issue reading or writing to the file
    """
    cached = True
    filename = 'cache/' + hashlib.sha256(USER_NAME.encode('utf-8')).hexdigest() + '.txt'

    try:
        with open(filename, 'r') as f:
            data = f.readlines()
    except FileNotFoundError:
        data = []
        if comment_size > 0:
            for _ in range(comment_size):
                data.append('This line is a comment block. Write whatever you want here.\n')
        with open(filename, 'w') as f:
            f.writelines(data)

    if len(data) - comment_size != len(edges) or force_cache:
        cached = False
        flush_cache(edges, filename, comment_size)
        with open(filename, 'r') as f:
            data = f.readlines()

    cache_comment = data[:comment_size]
    data = data[comment_size:]

    for index in range(len(edges)):
        repo_hash, commit_count, *__ = data[index].split()
        if repo_hash == hashlib.sha256(edges[index]['node']['nameWithOwner'].encode('utf-8')).hexdigest():
            try:
                if int(commit_count) != edges[index]['node']['defaultBranchRef']['target']['history']['totalCount']:
                    owner, repo_name = edges[index]['node']['nameWithOwner'].split('/')
                    loc = github.recursive_loc(owner, repo_name, data, cache_comment)
                    data[index] = (
                        repo_hash + ' ' +
                        str(edges[index]['node']['defaultBranchRef']['target']['history']['totalCount']) + ' ' +
                        str(loc[2]) + ' ' +
                        str(loc[0]) + ' ' +
                        str(loc[1]) + '\n'
                    )
            except TypeError:
                data[index] = repo_hash + ' 0 0 0 0\n'

    with open(filename, 'w') as f:
        f.writelines(cache_comment)
        f.writelines(data)

    for line in data:
        loc = line.split()
        loc_add += int(loc[3])
        loc_del += int(loc[4])

    return [loc_add, loc_del, loc_add - loc_del, cached]


def flush_cache(
    edges: list,
    filename: str,
    comment_size: int,
) -> None:
    """
    Wipes the cache file and recreates it with fresh data.

    Parameters
    ----------
    edges : list
        List of repository edges containing node information
    filename : str
        Path to the cache file
    comment_size : int
        Number of lines to preserve as comments

    Raises
    ------
    IOError
        If there is an issue writing to the file
    """
    with open(filename, 'r') as f:
        data = []
        if comment_size > 0:
            data = f.readlines()[:comment_size]

    with open(filename, 'w') as f:
        f.writelines(data)
        for node in edges:
            f.write(hashlib.sha256(node['node']['nameWithOwner'].encode('utf-8')).hexdigest() + ' 0 0 0 0\n')
