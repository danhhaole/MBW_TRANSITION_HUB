class CandidateCampaign:
    def __init__(self, candidate_id, campaign_id, status, enrolled_at, current_step_order, next_action_at):
        self.candidate_id = candidate_id
        self.campaign_id = campaign_id
        self.status = status
        self.enrolled_at = enrolled_at
        self.current_step_order = current_step_order
        self.next_action_at = next_action_at

    def update_status(self, new_status):
        self.status = new_status

    def advance_step(self):
        self.current_step_order += 1

    def set_next_action(self, next_action_time):
        self.next_action_at = next_action_time

    def get_candidate_progress(self):
        return {
            "candidate_id": self.candidate_id,
            "campaign_id": self.campaign_id,
            "status": self.status,
            "enrolled_at": self.enrolled_at,
            "current_step_order": self.current_step_order,
            "next_action_at": self.next_action_at
        }