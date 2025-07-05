def run_schedulers():
    from mbw_mira import tasks
    tasks.do_campaign_scheduler()
    tasks.do_candidate_campaign_scheduler()