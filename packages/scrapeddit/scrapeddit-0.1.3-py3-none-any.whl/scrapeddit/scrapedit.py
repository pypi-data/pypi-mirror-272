import tqdm
import praw
from datetime import datetime
import pandas as pd

class InvalidSubreddit(Exception):
    pass
class RestrictedSubreddit(Exception):
    pass
class AuthFailed(Exception):
   pass
class IncompleteAuth(Exception): pass
   
auths = []

def auth_reddit(client_id, client_secret, username, password, redirect_uri, user_agent, check_for_async = False):
  reddit = praw.Reddit(client_id = client_id,
            client_secret = client_secret,
            username = username,
            password = password,
            redirect_uri = redirect_uri,
            user_agent = user_agent,
            check_for_async=check_for_async)
  sub = reddit.subreddit('popular')
  try: sub_type = sub.subreddit_type
  except: raise InvalidSubreddit("Invalid Authentication, please recheck and try again")
  print("Authentication was successful")
  auths.append(reddit)

def scrape_reddit(subreddit: str, limit = 10, sortby = 'year', show_safe = None):
  if len(auths) == 0: raise IncompleteAuth("Complete Authentication by calling `scrapedit.auth_reddit` before proceeding")
  reddit = auths[0]
  sub = reddit.subreddit(subreddit)
  try:
    sub_type = sub.subreddit_type
    if sub_type != 'public':
      raise RestrictedSubreddit(f"r/{subreddit} is restricted to public access")
  except: raise InvalidSubreddit(f"r/{subreddit} is invalid Subreddit, make sure the subreddit is valid")
  result = []
  sub_itter = sub.top(sortby,limit = limit)
  for submission in tqdm(sub_itter):
    d = {}
    d['id'] = submission.id
    d['title'] = submission.title
    d['num_comments'] = submission.num_comments
    d['score'] = submission.score
    d['upvote_ratio'] = submission.upvote_ratio
    d['date'] = datetime.fromtimestamp(submission.created_utc)
    d['domain'] = submission.domain
    d['nsfw'] = submission.over_18
    try: d['image'] = submission.preview["images"][0]["source"]["url"]
    except: d['image'] = None
    try: d['author'] = submission.author.name
    except: d['author'] = 'Not Found'
    if show_safe == True and d['nsfw'] == True: d={}
    if show_safe == False and d['nsfw'] == False: d={}
    result.append(d)
  result = [item for item in result if item]
  return pd.DataFrame(result)