import statsapi
from datetime import date, timedelta
import praw

import config # this is where I store the PRAW credentials

def get_latest_scores(num_days=4):
    scores = []
    for x in range(num_days):
        today = (date.today() - timedelta(days=x)).strftime("%Y-%m-%d")
        team_id = 110
        schedule_data = statsapi.schedule(date=today, team=team_id)

        #text_template = f"Game ID: {game['game_id']} \n" \
        #                f"Date: {game['game_date']} " \
        #                f"{game['home_name']} ({game['home_score']}) :: " \
        #                f"{game['away_name']} ({game['away_score']}) :: " \

        if schedule_data:
            for game in schedule_data:
                #print(f"Game ID: {game['game_id']}")
                print(f"Date: {game['game_date']}",
                      f"{game['home_name']} ({game['home_score']})", "::",
                      f"{game['away_name']} ({game['away_score']})")
                #print("-" * 20)

                text_template = f"Date: {game['game_date']} " \
                                f"{game['home_name']} ({game['home_score']}) :: " \
                                f"{game['away_name']} ({game['away_score']}) :: "

                scores.append(text_template)
        else:
            print(f"No games found for team ID {team_id} on {today}.")
            #print("-" * 20)
            #scores.append(f"No games found for team ID {team_id} on {today}.")
    print('-' * 20)
    return scores

def get_latest_reddit_links(num_days):
    r = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
    )

    subreddit_name = "orioles"  # Replace with the subreddit you want to monitor
    target_flair_text = "Lucky Guess"  # Replace with the specific flair text you're looking for

    subreddit = r.subreddit(subreddit_name)
    flaired_posts = []
    lucky_guess_links = []

    for submission in subreddit.new(limit=100):
        if submission.link_flair_text == target_flair_text:
            flaired_posts.append(submission)

    print(f"Found {len(flaired_posts)} new posts with flair'{target_flair_text}':")
    for post in flaired_posts[:num_days]:
        link_text = post.permalink.split('/')[4]
        print(f"- {post.title} - {link_text}")
        lucky_guess_links.append(f"{post.title} - {link_text}")

    return lucky_guess_links

