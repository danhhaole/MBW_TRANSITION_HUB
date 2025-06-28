from datetime import datetime
from typing import Optional, Dict


class Action:
    def __init__(
        self,
        candidate_campaign_id: str,
        campaign_step: str,
        status: str,
        scheduled_at: Optional[datetime] = None,
        executed_at: Optional[datetime] = None,
        result: Optional[Dict] = None,
        assignee_id: Optional[str] = None,
    ):
        """
        Represents an Action entity.

        :param candidate_campaign_id: Foreign Key -> CandidateCampaign
        :param campaign_step: Foreign Key -> CampaignStep
        :param status: Status of the action (e.g., SCHEDULED, EXECUTED, etc.)
        :param scheduled_at: Datetime when the action is scheduled
        :param executed_at: Datetime when the action was executed
        :param result: JSON field to store the result of the action
        :param assignee_id: Foreign Key -> User
        """
        self.candidate_campaign_id = candidate_campaign_id
        self.campaign_step = campaign_step
        self.status = status
        self.scheduled_at = scheduled_at
        self.executed_at = executed_at
        self.result = result
        self.assignee_id = assignee_id

    def __repr__(self):
        return (
            f"Action(candidate_campaign_id={self.candidate_campaign_id}, "
            f"campaign_step={self.campaign_step}, status={self.status}, "
            f"scheduled_at={self.scheduled_at}, executed_at={self.executed_at}, "
            f"result={self.result}, assignee_id={self.assignee_id})"
        )