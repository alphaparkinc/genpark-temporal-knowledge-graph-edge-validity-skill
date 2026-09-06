import json
from client import TemporalKnowledgeGraphEdgeValidity

def main():
    tkg = TemporalKnowledgeGraphEdgeValidity()
    # Fact 1: Alice lived in Boston in 2024
    tkg.assert_fact("Alice", "lives_in", "Boston", valid_from="2024-01-01")
    # Fact 2: Alice moved to San Francisco in 2026
    tkg.assert_fact("Alice", "lives_in", "San Francisco", valid_from="2026-03-01")

    # Query historical point: 2025-06-01 -> should be Boston
    hist = tkg.query_point_in_time("2025-06-01")
    print("Historical Query (2025):", json.dumps(hist, indent=2))
    assert len(hist) == 1
    assert hist[0]["object"] == "Boston"

    # Query current point: 2026-09-01 -> should be San Francisco
    curr = tkg.query_point_in_time("2026-09-01")
    print("Current Query (2026):", json.dumps(curr, indent=2))
    assert len(curr) == 1
    assert curr[0]["object"] == "San Francisco"
    print("Temporal knowledge graph verification: PASS")

if __name__ == "__main__":
    main()
