#!/usr/bin/env python3
from config import settings
import click
from linkedin_api import Linkedin
import json

@click.group()
@click.option('-u', '--li-username', 'username', default=settings.linkedin_username, type=str,
        help="Username for your LinkedIn account")
@click.option('-p', '--li-password', 'password',
        default=settings.linkedin_password, type=str,
        help='Password for your LinkedIn account')
@click.option('-v', '--verbose', 'verbose',
        default=False, type=bool,
        help='Increase verbosity')
@click.pass_context
def cli(ctx, username, password, verbose):
    """Run commands against a LinkedIn account"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['api'] = Linkedin(username, password, debug=verbose)

@cli.command()
@click.pass_context
def show_mini_profile(ctx):
    """Show connected LinkedIn "mini" Profile"""
    api = ctx.obj['api']
    profile = api.get_user_profile()
    click.echo(json.dumps(profile, indent=2))

@cli.command()
@click.pass_context
def show_full_profile(ctx):
    """Show connected LinkedIn "full" Profile"""
    api = ctx.obj['api']
    mini_profile = api.get_user_profile()
    # profileId = mini_profile.get('plainId')
    # profileUrn = mini_profile.get('miniProfile').get('objectUrn')
    profileEntityUrn = mini_profile.get('miniProfile').get('entityUrn')
    profileUuid = profileEntityUrn.split(':')[-1]
    response = api._fetch(f"/identity/profiles/${profileUuid}").json()
    click.echo(json.dumps(response, indent=2))

@cli.command()
@click.pass_context
def show_profile_updates(ctx):
    """Show connected LinkedIn profile updates (newsfeed)"""
    api = ctx.obj['api']
    mini_profile = api.get_user_profile()
    profileId = mini_profile.get('plainId')
    response = api.get_profile_updates(profileId)
    click.echo(json.dumps(response, indent=2))

# Borrow this implementation from development version:
# https://github.com/tomquirk/linkedin-api/blob/master/linkedin_api/linkedin.py
@cli.command()
@click.pass_context
def show_feed_activity(ctx):
    """Dump raw data from activity feed for post-processing."""
    api = ctx.obj['api']
    l_posts = []
    l_urns = []
    offset = 0

    # If count>100 API will return HTTP 400
    count = api._MAX_UPDATE_COUNT
    limit = api._MAX_UPDATE_COUNT

    while True:

        # when we're close to the limit, only fetch what we need to
        if limit > -1 and limit - len(l_urns) < count:
            count = limit - len(l_urns)
        params = {
            "count": str(count),
            "q": "chronFeed",
            "start": len(l_urns) + offset,
        }
        res = api._fetch(
            f"/feed/updatesV2",
            params=params,
            headers={"accept": "application/vend.linkedin.normalized+json+2.1"},
        ).json()

        l_raw_posts = res.get("included", {})
        l_raw_urns = res.get("data", {}).get("*elements", [])
        l_posts.extend(l_raw_posts)
        l_urns.extend(l_raw_urns)
        if (
            (limit > -1 and len(l_urns) >= limit)  # if our results exceed set limit
            or len(l_urns) / count >= api._MAX_REPEATED_REQUESTS
            ) or len(l_raw_urns) == 0:
            break

    click.echo(json.dumps(l_posts, indent=2))
    # click.echo(l_urns)


@cli.command()
@click.pass_context
def get_conversations(ctx):
    """Show conversations active in connected LinkedIn Profile"""
    api = ctx.obj['api']
    response = api.get_conversations()
    click.echo(json.dumps(response, indent=2))

@cli.command()
@click.pass_context
def show_profile_connections(ctx):
    """Show profile connections"""
    api = ctx.obj['api']
    mini_profile = api.get_user_profile()
    profileUrn = mini_profile.get('miniProfile').get('objectUrn')
    response = api.get_profile_connections(profileUrn)
    click.echo(json.dumps(response, indent=2))

## TODO - enable engagement queries
# https://github.com/tomquirk/linkedin-api/issues/65
def get_likers(ctx, thread_id=None):
    res = ctx._fetch(f"/feed/reactions?count=10&q=reactionType&start=10&threadUrn={thread_id}")
    return res.json()

# Hide this command - it's mostly useful in development
@cli.command(hidden=True)
@click.pass_context
def show_methods(ctx):
    """Show methods available on the LinkedIn object"""
    api = ctx.obj['api']
    click.echo([x for x in dir(api) if not x.startswith('_')])

# Borrow this implementation from the development version.
# It could be replaced by
# response = api.get_profile_posts(urn_id = profileUrn, post_count=count)
# https://github.com/tomquirk/linkedin-api/blob/master/linkedin_api/linkedin.py#L99
# Note - installing from git using
#  % pipenv install -e git+https://github.com/tomquirk/linkedin-api/#egg=linkedin-api
# did not give better results.
@cli.command()
@click.option('--count', default=10, type=int, help='Number of posts to fetch for user.')
@click.pass_context
def get_profile_posts(ctx, count):
    """Get COUNT posts from the user's profile"""
    api = ctx.obj['api']
    mini_profile = api.get_user_profile()
    profileUrn = mini_profile.get('miniProfile').get('objectUrn')
    params = {
        "count": min(count, 100),
        "start": 0,
        "q": "memberShareFeed",
        "moduleKey": "member-shares:phone",
        "includeLongTermHistory": True,
        "profileUrn": profileUrn,
    }
    url = f"/identity/profileUpdatesV2"
    res = api._fetch(url, params=params)
    data = res.json()
    if data and "status" in data and data["status"] != 200:
        api.logger.info("request failed: {}".format(data["message"]))
        return {}
    while data and data["metadata"]["paginationToken"] != "":
        if len(data["elements"]) >= count:
            break
        pagination_token = data["metadata"]["paginationToken"]
        params["start"] = params["start"] + 100
        params["paginationToken"] = pagination_token
        res = api._fetch(url, params=params)
        data["metadata"] = res.json()["metadata"]
        data["elements"] = data["elements"] + res.json()["elements"]
        data["paging"] = res.json()["paging"]
    click.echo(json.dumps(data, indent=2))


if __name__ == "__main__":
    cli(obj={})
