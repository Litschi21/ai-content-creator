import json
import praw

filename = "E:/Desk/Programming/portfolio-projects/ai-content-creator/data/settings.json"

def load_settings():
    with open(filename, "r") as f:
        data = json.load(f)

        comment_amt = data["Comment Amount"]
        post_amt = data["Post Amount"]
        subreddit = data["Subreddit"]

        return comment_amt, post_amt, subreddit

def fetch_posts(status):
    titles = []
    descriptions = []
    comments = []
    comments_collected = 0

    comment_amt, post_amt, subreddit = load_settings()

    if status:
        status.config(text="Fetching posts")

    for submission in r.subreddit(subreddit).top(limit=int(post_amt)+100, time_filter="day"):
        if submission.stickied or submission.over_18 or hasattr(submission, 'post_hint') and submission.post_hint == 'image':
            continue

        if len(titles) >= int(post_amt):
            break

        titles.append(submission.title)

        if submission.selftext:
            descriptions.append(submission.selftext)

        submission.comments.replace_more(limit=1)
        for comment in submission.comments.list():
            if comments_collected >= int(comment_amt):
                break
            
            if comment.author and comment.author.name.lower() == "automoderator":
                continue

            comments.append(comment.body)
            comments_collected += 1
        
        print(f'Fetched {len(comments)} comments from post: "{submission.title}"')
        print(f'Fetched {len(descriptions)} descriptions from post: "{submission.title}"\n')
    print(f'Fetched {len(titles)} posts from subreddit: "{subreddit}"')

    return comments, descriptions, titles

r = praw.Reddit(
    client_id="client-id",
    client_secret="client-secret",
    user_agent="user-agent",
)
