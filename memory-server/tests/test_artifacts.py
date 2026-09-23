from bot_memory_server.artifacts import build_artifacts


def test_build_artifacts_includes_related_jira_keys_and_pull_requests(monkeypatch):
    monkeypatch.setattr("bot_memory_server.artifacts.JIRA_BASE_URL", "https://redhat.atlassian.net/browse")

    artifacts = build_artifacts(
        {
            "related_jira_keys": ["OCPBUGS-127374", "OCPBUGS-127077"],
            "prs": [{"number": 17203, "url": "https://github.com/openshift/console/pull/17203"}],
        }
    )

    assert artifacts == [
        {
            "name": "OCPBUGS-127374",
            "url": "https://redhat.atlassian.net/browse/OCPBUGS-127374",
            "type": "jira_issue",
        },
        {
            "name": "OCPBUGS-127077",
            "url": "https://redhat.atlassian.net/browse/OCPBUGS-127077",
            "type": "jira_issue",
        },
        {
            "name": "PR #17203",
            "url": "https://github.com/openshift/console/pull/17203",
            "type": "pull_request",
        },
    ]


def test_build_artifacts_deduplicates_related_jira_keys(monkeypatch):
    monkeypatch.setattr("bot_memory_server.artifacts.JIRA_BASE_URL", "https://redhat.atlassian.net/browse")

    artifacts = build_artifacts({"related_jira_keys": ["REHOR-160", "REHOR-160"]})

    assert len(artifacts) == 1
