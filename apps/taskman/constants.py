from osidb.helpers import get_env

TASKMAN_API_VERSION = "v1"

JIRA_TASKMAN_URL = get_env("JIRA_TASKMAN_URL")
JIRA_TASKMAN_PROJECT_KEY = get_env("JIRA_TASKMAN_PROJECT_KEY", default="OSIM")
HTTPS_TASKMAN_PROXY = get_env("HTTPS_TASKMAN_PROXY")
