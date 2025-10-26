from chalkbox import Alert, StatusCard


class TestStatusCard:
    """Tests for StatusCard component."""

    def test_status_card_creation(self):
        """Test basic status card creation."""
        card = StatusCard(title="Test Service", status="healthy")
        assert card.title == "Test Service"
        assert card.status == "healthy"

    def test_status_card_with_metrics(self):
        """Test status card with metrics."""
        metrics = {"Uptime": "24d 5h", "Connections": "42/100"}
        card = StatusCard(title="Database", status="healthy", metrics=metrics)
        assert card.metrics == metrics

    def test_status_card_with_bars(self):
        """Test status card with bars."""
        bars = [("CPU", 45.0, 100.0), ("Memory", 67.0, 100.0)]
        card = StatusCard(title="Server", status="warning", bars=bars)
        assert len(card.bars) == 2
        assert card.bars[0] == ("CPU", 45.0, 100.0)

    def test_status_card_with_alert(self):
        """Test status card with alert."""
        alert = Alert.warning("High memory usage")
        card = StatusCard(title="Server", status="warning", alert=alert)
        assert card.alert == alert

    def test_status_card_with_subtitle(self):
        """Test status card with subtitle."""
        card = StatusCard(title="API Gateway", status="healthy", subtitle="v2.1.0")
        assert card.subtitle == "v2.1.0"

    def test_status_glyph(self):
        """Test status indicator glyphs."""
        healthy = StatusCard(title="Test", status="healthy")
        assert healthy._get_status_glyph() == "✓"

        warning = StatusCard(title="Test", status="warning")
        assert warning._get_status_glyph() == "⚠"

        error = StatusCard(title="Test", status="error")
        assert error._get_status_glyph() == "✖"

        unknown = StatusCard(title="Test", status="unknown")
        assert unknown._get_status_glyph() == "?"

    def test_bar_severity_calculation(self):
        """Test bar severity calculation based on thresholds."""
        card = StatusCard(title="Test", status="healthy")
        assert card._get_bar_severity("cpu", 50.0, 100.0) == "success"
        assert card._get_bar_severity("cpu", 75.0, 100.0) == "success"
        assert card._get_bar_severity("cpu", 95.0, 100.0) == "success"

        thresholds = {"cpu": (70.0, 90.0)}
        card_with_thresholds = StatusCard(
            title="Test", status="healthy", bar_thresholds=thresholds
        )

        assert card_with_thresholds._get_bar_severity("cpu", 50.0, 100.0) == "success"
        assert card_with_thresholds._get_bar_severity("cpu", 75.0, 100.0) == "warning"
        assert card_with_thresholds._get_bar_severity("cpu", 95.0, 100.0) == "error"

    def test_bar_severity_with_custom_thresholds(self):
        """Test bar severity with custom thresholds."""
        custom_thresholds = {"custom_metric": (50.0, 80.0)}
        card = StatusCard(title="Test", status="healthy", bar_thresholds=custom_thresholds)

        assert card._get_bar_severity("custom_metric", 40.0, 100.0) == "success"
        assert card._get_bar_severity("custom_metric", 60.0, 100.0) == "warning"
        assert card._get_bar_severity("custom_metric", 85.0, 100.0) == "error"

    def test_from_health_check(self):
        """Test creating StatusCard from health check data."""
        health_data = {
            "status": "healthy",
            "uptime": "24d 5h 32m",
            "connections": "42/100",
            "response_time": "12ms",
        }
        card = StatusCard.from_health_check("Database", health_data)
        assert card.title == "Database"
        assert card.status == "healthy"
        assert card.metrics["uptime"] == "24d 5h 32m"

    def test_from_health_check_status_normalization(self):
        """Test status normalization in from_health_check."""
        test_cases = [
            ("ok", "healthy"),
            ("success", "healthy"),
            ("warn", "warning"),
            ("fail", "error"),
            ("failed", "error"),
            ("critical", "error"),
            ("unknown", "unknown"),
            ("invalid_status", "unknown"),
        ]

        for input_status, expected_status in test_cases:
            health_data = {"status": input_status}
            card = StatusCard.from_health_check("Service", health_data)
            assert card.status == expected_status

    def test_from_health_check_with_bars(self):
        """Test from_health_check with bars."""
        health_data = {
            "status": "warning",
            "bars": [("CPU", 75.0, 100.0), ("Memory", 85.0, 100.0)],
        }
        card = StatusCard.from_health_check("Server", health_data)
        assert len(card.bars) == 2

    def test_explicit_bar_severity(self):
        """Test bars with explicit severity (4-tuple format)."""
        bars = [
            ("Throughput", 85.0, 100.0, "warning"),
            ("Response Time", 145.0, 200.0, "success"),
            ("Error Rate", 5.0, 100.0, "error"),
        ]
        card = StatusCard(title="API Gateway", status="warning", bars=bars)
        assert len(card.bars) == 3
        renderable = card.__rich__()
        assert renderable is not None

    def test_mixed_bar_formats(self):
        """Test mixing 3-tuple and 4-tuple bar formats."""
        bars = [
            ("CPU", 75.0, 100.0),              # 3-tuple, severity calculated from thresholds
            ("Memory", 85.0, 100.0, "error"),  # 4-tuple, explicit severity
        ]
        thresholds = {"CPU": (70.0, 90.0)}
        card = StatusCard(title="Server", status="warning", bars=bars, bar_thresholds=thresholds)
        renderable = card.__rich__()
        assert renderable is not None

    def test_rich_renderable(self):
        """Test that StatusCard is a Rich renderable."""
        card = StatusCard(title="Test", status="healthy")
        renderable = card.__rich__()
        assert renderable is not None

    def test_fail_safe_behavior(self):
        """Test fail-safe behavior with invalid data."""
        # Should not raise exceptions
        card = StatusCard(title="Test", status="healthy", bars=[("Invalid", -1.0, 0.0)])
        renderable = card.__rich__()
        assert renderable is not None

    def test_empty_status_card(self):
        """Test status card with no metrics or bars."""
        card = StatusCard(title="Empty Service", status="unknown")
        renderable = card.__rich__()
        assert renderable is not None

    def test_expand_option(self):
        """Test expand option for full-width sections."""
        card = StatusCard(title="Test", status="healthy", expand=True)
        assert card.expand is True

        card_compact = StatusCard(title="Test", status="healthy", expand=False)
        assert card_compact.expand is False
