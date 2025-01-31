import datetime
from dateutil import relativedelta
import os
from lxml import etree
from pathlib import Path

# Import modules.
from utils import formatter, timer
from graphql.github import *
from svg import svg
from config import environment

# Fine-grained personal access token with All Repositories access:
# Account permissions: read:Followers, read:Starring, read:Watching
# Repository permissions: read:Commit statuses, read:Contents, read:Issues, read:Metadata, read:Pull Requests
# Issues and pull requests permissions not needed at the moment, but may be used in the future

def daily_readme(birthday: datetime.datetime) -> str:
    """
    Returns the length of time since the given birthday
    e.g., 'XX years, XX months, XX days'
    """
    diff: relativedelta.relativedelta = relativedelta.relativedelta(datetime.datetime.today(), birthday)
    return '{} {}, {} {}, {} {}{}'.format(
        diff.years, 'year' + formatter.toPlural(diff.years),
        diff.months, 'month' + formatter.toPlural(diff.months),
        diff.days, 'day' + formatter.toPlural(diff.days),
        ' 🎂' if (diff.months == 0 and diff.days == 0) else ''
    )

if __name__ == '__main__':
    """
    """
    env = environment.EnvironmentConfig()
    env.load_env_vars()
    
    USER_NAME: str = env.USER_NAME
    OUTPUT_PATH: str = env.OUTPUT_PATH
    BIRTHDAY: datetime = env.BIRTHDAY
    
    print('Calculation times:')
    # define global variable for owner ID and calculate user's creation date
    # e.g {'id': 'MDQ6VXNlcjU3MzMxMTM0'} and 2019-11-03T21:15:07Z for username 'Andrew6rant'
    user_data, user_time = timer.perf_counter(user_getter, USER_NAME)
    OWNER_ID, acc_date = user_data
    set_owner_id(OWNER_ID)
    formatter.timeDiffFormatted('account data', user_time)
    age_data, age_time = timer.perf_counter(daily_readme, BIRTHDAY)
    formatter.timeDiffFormatted('age calculation', age_time)
    total_loc, loc_time = timer.perf_counter(loc_query, ['OWNER', 'COLLABORATOR', 'ORGANIZATION_MEMBER'], 7)
    formatter.timeDiffFormatted('LOC (cached)', loc_time) if total_loc[-1] else formatter.timeDiffFormatted('LOC (no cache)', loc_time)
    
    commit_data, commit_time = timer.perf_counter(commit_counter, 7)
    star_data, star_time = timer.perf_counter(graph_repos_stars, 'stars', ['OWNER'])
    repo_data, repo_time = timer.perf_counter(graph_repos_stars, 'repos', ['OWNER'])
    contrib_data, contrib_time = timer.perf_counter(graph_repos_stars, 'repos', ['OWNER', 'COLLABORATOR', 'ORGANIZATION_MEMBER'])
    follower_data, follower_time = timer.perf_counter(follower_getter, USER_NAME)

    # several repositories that I've contributed to have since been deleted.
    print(f"OWNER_ID: {OWNER_ID}")
    if OWNER_ID == {'id': 'MDQ6VXNlcjg1NTQ21'}: # only calculate for user Andrew6rant
        archived_data = add_archive()
        for index in range(len(total_loc)-1):
            total_loc[index] += archived_data[index]
        contrib_data += archived_data[-1]
        commit_data += int(archived_data[-2])

    for index in range(len(total_loc)-1): total_loc[index] = '{:,}'.format(total_loc[index]) # format added, deleted, and total LOC

    svg.svg_overwrite(Path('output/' + 'dark_mode.svg').resolve(), age_data, commit_data, star_data, repo_data, contrib_data, follower_data, total_loc[:-1])
    svg.svg_overwrite(Path('output/' + 'light_mode.svg').resolve(), age_data, commit_data, star_data, repo_data, contrib_data, follower_data, total_loc[:-1])

    # move cursor to override 'Calculation times:' with 'Total function time:' and the total function time, then move cursor back
    print('\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F',
        '{:<21}'.format('Total function time:'), '{:>11}'.format('%.4f' % (user_time + age_time + loc_time + commit_time + star_time + repo_time + contrib_time)),
        ' s \033[E\033[E\033[E\033[E\033[E\033[E\033[E\033[E', sep='')

    print('Total GitHub GraphQL API calls:', '{:>3}'.format(sum(QUERY_COUNT.values())))
    for funct_name, count in QUERY_COUNT.items(): print('{:<28}'.format('   ' + funct_name + ':'), '{:>6}'.format(count))
