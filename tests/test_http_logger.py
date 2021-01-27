# coding: utf-8
# © 2016-2021 Resurface Labs Inc.

from test_helper import *

from usagelogger import HttpLogger, UsageLoggers


def test_creates_instance():
    logger = HttpLogger()
    assert logger is not None
    assert logger.agent == HttpLogger.AGENT
    assert logger.enableable is False
    assert logger.enabled is False
    assert logger.queue is None
    assert logger.url is None


def test_creates_multiple_instances():
    url1 = "https://resurface.io"
    url2 = "https://whatever.com"
    logger1 = HttpLogger(url=url1)
    logger2 = HttpLogger(url=url2)
    logger3 = HttpLogger(url=DEMO_URL)

    assert logger1.agent == HttpLogger.AGENT
    assert logger1.enableable is True
    assert logger1.enabled is True
    assert logger1.url == url1
    assert logger2.agent == HttpLogger.AGENT
    assert logger2.enableable is True
    assert logger2.enabled is True
    assert logger2.url == url2
    assert logger3.agent == HttpLogger.AGENT
    assert logger3.enableable is True
    assert logger3.enabled is True
    assert logger3.url == DEMO_URL

    UsageLoggers.disable()
    assert UsageLoggers.is_enabled() is False
    assert logger1.enabled is False
    assert logger2.enabled is False
    assert logger3.enabled is False
    UsageLoggers.enable()
    assert UsageLoggers.is_enabled() is True
    assert logger1.enabled is True
    assert logger2.enabled is True
    assert logger3.enabled is True


def test_detects_string_content_types():
    assert HttpLogger.is_string_content_type(None) is False
    assert HttpLogger.is_string_content_type("") is False
    assert HttpLogger.is_string_content_type(" ") is False
    assert HttpLogger.is_string_content_type("/") is False
    assert HttpLogger.is_string_content_type("application/") is False
    assert HttpLogger.is_string_content_type("json") is False
    assert HttpLogger.is_string_content_type("html") is False
    assert HttpLogger.is_string_content_type("xml") is False

    assert HttpLogger.is_string_content_type("application/json") is True
    assert HttpLogger.is_string_content_type("application/soap") is True
    assert HttpLogger.is_string_content_type("application/xml") is True
    assert (
        HttpLogger.is_string_content_type("application/x-www-form-urlencoded") is True
    )
    assert HttpLogger.is_string_content_type("text/html") is True
    assert HttpLogger.is_string_content_type("text/html; charset=utf-8") is True
    assert HttpLogger.is_string_content_type("text/plain") is True
    assert HttpLogger.is_string_content_type("text/plain123") is True
    assert HttpLogger.is_string_content_type("text/xml") is True
    assert HttpLogger.is_string_content_type("Text/XML") is True


def test_has_valid_agent():
    agent = HttpLogger.AGENT
    assert len(agent) > 0
    assert agent.endswith(".py")
    assert ("\\" in agent) is False
    assert ('"' in agent) is False
    assert ("'" in agent) is False
    assert HttpLogger().agent == agent


def test_silently_ignores_unexpected_option_classes():
    logger = HttpLogger(DEMO_URL)
    assert logger.enableable is False
    assert logger.enabled is False
    assert logger.queue is None
    assert logger.url is None

    logger = HttpLogger(True)
    assert logger.enableable is False
    assert logger.enabled is False
    assert logger.queue is None
    assert logger.url is None

    logger = HttpLogger([])
    assert logger.enableable is False
    assert logger.enabled is False
    assert logger.queue is None
    assert logger.url is None

    logger = HttpLogger(url=[])
    assert logger.enableable is False
    assert logger.enabled is False
    assert logger.queue is None
    assert logger.url is None

    logger = HttpLogger(url=23)
    assert logger.enableable is False
    assert logger.enabled is False
    assert logger.queue is None
    assert logger.url is None

    logger = HttpLogger(queue="asdf")
    assert logger.enableable is False
    assert logger.enabled is False
    assert logger.queue is None
    assert logger.url is None

    logger = HttpLogger(queue=45)
    assert logger.enableable is False
    assert logger.enabled is False
    assert logger.queue is None
    assert logger.url is None

    logger = HttpLogger(enabled=2)
    assert logger.enableable is False
    assert logger.enabled is False
    assert logger.queue is None
    assert logger.url is None
