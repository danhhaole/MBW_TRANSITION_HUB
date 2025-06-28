class CampaignStep:
    def __init__(self, campaign, step_order, action_type, delay_in_days, template, action_config):
        self.campaign = campaign
        self.step_order = step_order
        self.action_type = action_type
        self.delay_in_days = delay_in_days
        self.template = template
        self.action_config = action_config

    def execute(self):
        if self.action_type == "SEND_EMAIL":
            return self.send_email()
        elif self.action_type == "SEND_SMS":
            return self.send_sms()
        elif self.action_type == "MANUAL_CALL":
            return self.manual_call()
        elif self.action_type == "MANUAL_TASK":
            return self.manual_task()
        else:
            raise ValueError("Invalid action type")

    def send_email(self):
        # Logic for sending email
        pass

    def send_sms(self):
        # Logic for sending SMS
        pass

    def manual_call(self):
        # Logic for manual call
        pass

    def manual_task(self):
        # Logic for manual task
        pass