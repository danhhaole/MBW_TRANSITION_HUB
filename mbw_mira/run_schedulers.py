def run_schedulers():
    from mbw_mira.services.scheduler_engine import CampaignSchedulerEngine
    CampaignSchedulerEngine().run()
