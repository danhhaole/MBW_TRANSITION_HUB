class Mira Segment:
    def __init__(self, segment_name, criteria):
        self.segment_name = segment_name
        self.criteria = criteria

    def update_criteria(self, new_criteria):
        self.criteria = new_criteria

    def get_segment_info(self):
        return {
            "segment_name": self.segment_name,
            "criteria": self.criteria
        }