class CandidateSegment:
    def __init__(self, criteria):
        self.criteria = criteria

    def add_criteria(self, new_criteria):
        self.criteria.append(new_criteria)

    def remove_criteria(self, criteria_to_remove):
        self.criteria.remove(criteria_to_remove)

    def get_segment_info(self):
        return {
            "criteria": self.criteria
        }