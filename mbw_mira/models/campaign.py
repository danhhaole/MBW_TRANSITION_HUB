class Campaign:
    def __init__(self, campaign_name, campaign_type, status, target_segment, start_date, end_date):
        self.campaign_name = campaign_name
        self.type = campaign_type
        self.status = status
        self.target_segment = target_segment
        self.start_date = start_date
        self.end_date = end_date

    def update_status(self, new_status):
        self.status = new_status

    def extend_campaign(self, new_end_date):
        self.end_date = new_end_date

    def get_campaign_details(self):
        return {
            "campaign_name": self.campaign_name,
            "type": self.type,
            "status": self.status,
            "target_segment": self.target_segment,
            "start_date": self.start_date,
            "end_date": self.end_date
        }