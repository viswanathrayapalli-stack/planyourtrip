from app.shared.metrics.request_metrics import RequestMetrics


def test_empty_snapshot_returns_zero_values() -> None:
    metrics = RequestMetrics()

    snapshot = metrics.snapshot()

    assert snapshot["total_requests"] == 0
    assert snapshot["requests_by_method"] == {}
    assert snapshot["requests_by_status"] == {}
    assert snapshot["requests_by_path"] == {}
    assert snapshot["total_duration_ms"] == 0.0
    assert snapshot["average_duration_ms"] == 0.0


def test_record_completed_request_updates_request_statistics() -> None:
    metrics = RequestMetrics()

    metrics.record_completed_request(
        method="GET",
        path="/health",
        status_code=200,
        duration_ms=25.0,
    )

    snapshot = metrics.snapshot()

    assert snapshot["total_requests"] == 1
    assert snapshot["requests_by_method"] == {"GET": 1}
    assert snapshot["requests_by_status"] == {"200": 1}
    assert snapshot["requests_by_path"] == {"/health": 1}
    assert snapshot["total_duration_ms"] == 25.0
    assert snapshot["average_duration_ms"] == 25.0


def test_record_completed_request_aggregates_statistics() -> None:
    metrics = RequestMetrics()

    metrics.record_completed_request(method="GET", path="/health", status_code=200, duration_ms=10.0)
    metrics.record_completed_request(method="GET", path="/health", status_code=200, duration_ms=20.0)
    metrics.record_completed_request(method="POST", path="/api/v1/trips", status_code=201, duration_ms=30.0)
    metrics.record_completed_request(method="GET", path="/api/v1/trips", status_code=404, duration_ms=40.0)

    snapshot = metrics.snapshot()

    assert snapshot["total_requests"] == 4
    assert snapshot["requests_by_method"] == {"GET": 3, "POST": 1}
    assert snapshot["requests_by_status"] == {"200": 2, "201": 1, "404": 1}
    assert snapshot["requests_by_path"] == {
        "/health": 2,
        "/api/v1/trips": 2,
    }
    assert snapshot["total_duration_ms"] == 100.0
    assert snapshot["average_duration_ms"] == 25.0


def test_snapshot_returns_independent_dictionaries() -> None:
    metrics = RequestMetrics()
    metrics.record_completed_request(method="GET", path="/health", status_code=200, duration_ms=10.0)

    snapshot = metrics.snapshot()
    snapshot["requests_by_method"]["GET"] = 999
    snapshot["requests_by_status"]["200"] = 999
    snapshot["requests_by_path"]["/health"] = 999

    subsequent_snapshot = metrics.snapshot()

    assert subsequent_snapshot["requests_by_method"] == {"GET": 1}
    assert subsequent_snapshot["requests_by_status"] == {"200": 1}
    assert subsequent_snapshot["requests_by_path"] == {"/health": 1}
