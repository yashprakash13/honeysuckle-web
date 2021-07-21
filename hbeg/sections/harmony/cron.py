from .dailyfeed.feedmaker import FeedMaker


def feed_ao3_scheduled_job():
    """cron job to get new ao3 feed every 12 hours"""
    print("Executing crob job for harmony feed...")
    _ = FeedMaker(refresh=True)
