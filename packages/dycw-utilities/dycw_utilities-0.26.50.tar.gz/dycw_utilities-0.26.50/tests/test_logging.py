from __future__ import annotations

from logging import getLogger

from utilities.logging import LogLevel, basic_config


class TestBasicConfig:
    def test_main(self) -> None:
        basic_config()
        logger = getLogger(__name__)
        logger.info("message")


class TestLogLevel:
    def test_main(self) -> None:
        assert len(LogLevel) == 5
