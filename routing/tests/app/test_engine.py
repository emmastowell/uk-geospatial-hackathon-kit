from routing_app.engine import LIMIT_COSTINGS, summarise_limits


def test_summarise_limits_reports_counts_and_kilometres() -> None:
    costing = {
        "max_locations": 20,
        "max_distance": 5_000_000.0,
        "max_matrix_location_pairs": 2500,
        "max_matrix_distance": 2_000_000.0,
    }
    service_limits = {
        **{name: costing for name in LIMIT_COSTINGS},
        "isochrone": {"max_contours": 4, "max_time_contour": 120, "max_distance_contour": 200},
        "trace": {"max_shape": 16000, "max_distance": 200_000.0},
    }

    limits = summarise_limits(service_limits)

    assert limits["costing"]["auto"] == {
        "route_locations": 20,
        "route_km": 5000,
        "matrix_pairs": 2500,
        "matrix_km": 2000,
    }
    assert limits["isochrone"] == {"contours": 4, "minutes": 120, "km": 200}
    assert limits["trace"] == {"points": 16000, "km": 200}
