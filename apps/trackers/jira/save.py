"""
Jira tracker query module
"""
import json
import logging

from collectors.jiraffe.core import JiraQuerier

from . import TrackerJiraQueryBuilder
from .constants import JIRA_SERVER

logger = logging.getLogger(__name__)


class TrackerJiraSaver(JiraQuerier):
    """
    Jira tracker bug save handler
    """

    def __init__(self, token) -> None:
        """
        Instantiate a new JiraTrackerQuerier object.

        Keyword arguments:
        token -- user token used in every request to Jira
        """
        self._jira_server = JIRA_SERVER
        self._jira_token = token

    def create(self, tracker):
        """
        create a representation of tracker model in Jira
        """
        query = TrackerJiraQueryBuilder(tracker).generate()
        issue = self.jira_conn.create_issue(fields=query["fields"], prefetch=True)
        tracker.external_system_id = issue["key"]
        return tracker

    def update(self, tracker):
        """
        update an existing representation of tracker model in Jira
        """
        query = TrackerJiraQueryBuilder(tracker).generate()
        url = f"{self.jira_conn._get_url('issue')}/{query['key']}"
        self.jira_conn._session.put(url, json.dumps(query))
