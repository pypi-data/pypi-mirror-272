"""
Upload script called by Github Actions
"""

import sys

from test_behavior_curriculum import curriculum

USER_CURRICULUM = curriculum.construct_track_curriculum()

if __name__ == "__main__":
    if not (USER_CURRICULUM is None):
        # Github Actions uploads contents of tmp_dir to S3
        tmp_dir = sys.argv[1]
        USER_CURRICULUM.export_curriculum(tmp_dir)