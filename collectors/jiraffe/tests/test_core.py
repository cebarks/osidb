import pytest
from django.utils import timezone
from jira import Issue

from collectors.jiraffe.core import JiraQuerier
from collectors.jiraffe.exceptions import NonRecoverableJiraffeException

pytestmark = pytest.mark.unit


class TestJiraQuerier:
    """
    test that Jira queries work
    """

    @pytest.mark.vcr
    def test_get_issue(self):
        """
        test that getting the given Jira issue works
        """
        tracker = JiraQuerier().get_issue("ENTESB-8726")

        assert isinstance(tracker, Issue)
        assert tracker.key == "ENTESB-8726"

    @pytest.mark.vcr
    def test_get_issue_non_accessible(self):
        """
        test getting a non-accessible Jira issue
        """
        with pytest.raises(
            NonRecoverableJiraffeException,
            match="Issue access is restricted or it does not exist",
        ):
            JiraQuerier().get_issue("AA-863")

    @pytest.mark.vcr
    def test_get_issue_non_existing(self):
        """
        test getting a non-exisiting Jira issue
        """
        with pytest.raises(
            NonRecoverableJiraffeException,
            match="Issue access is restricted or it does not exist",
        ):
            JiraQuerier().get_issue("TESTING-NONSENSE")

    @pytest.mark.vcr
    def test_get_tracker_period(self):
        """
        test that getting the Jira issues in the give period works
        """
        from_dt = timezone.datetime(2014, 6, 16, 0, 0, 0, tzinfo=timezone.utc)
        till_dt = timezone.datetime(2014, 9, 19, 0, 0, 0, tzinfo=timezone.utc)
        trackers = JiraQuerier().get_tracker_period(from_dt, till_dt)

        assert len(trackers) == 5
        assert all(isinstance(tracker, Issue) for tracker in trackers)
        assert sorted(tracker.key for tracker in trackers) == [
            "ENTESB-1766",
            "ENTESB-1767",
            "ENTMQ-701",
            "ENTMQ-754",
            "ENTMQ-755",
        ]
