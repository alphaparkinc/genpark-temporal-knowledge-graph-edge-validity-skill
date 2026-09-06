import datetime
from typing import Dict, Any, List, Optional

class TemporalKnowledgeGraphEdgeValidity:
    """
    Manages knowledge graph relationships with bitemporal intervals (valid_from, valid_to).
    Automatically retires outdated facts when contradictory relationships are asserted.
    """
    def __init__(self):
        self.edges: List[Dict[str, Any]] = []

    def assert_fact(
        self,
        subject: str,
        predicate: str,
        obj: str,
        valid_from: str,
        valid_to: Optional[str] = None
    ) -> Dict[str, Any]:
        # Expire any conflicting existing active edge with same subject & predicate
        retired_count = 0
        for edge in self.edges:
            if edge["subject"] == subject and edge["predicate"] == predicate and edge["valid_to"] is None:
                edge["valid_to"] = valid_from
                retired_count += 1

        new_edge = {
            "edge_id": f"edge_{len(self.edges) + 1:04d}",
            "subject": subject,
            "predicate": predicate,
            "object": obj,
            "valid_from": valid_from,
            "valid_to": valid_to,
            "recorded_at": datetime.date.today().isoformat()
        }
        self.edges.append(new_edge)

        return {
            "status": "ASSERTED",
            "edge_id": new_edge["edge_id"],
            "retired_previous_facts": retired_count,
            "new_fact": f"{subject} {predicate} {obj} [from: {valid_from}]"
        }

    def query_point_in_time(self, query_date: str) -> List[Dict[str, Any]]:
        q_dt = datetime.date.fromisoformat(query_date)
        active = []
        for edge in self.edges:
            vf = datetime.date.fromisoformat(edge["valid_from"])
            vt = datetime.date.fromisoformat(edge["valid_to"]) if edge["valid_to"] else None
            
            if vf <= q_dt and (vt is None or q_dt < vt):
                active.append(edge)
        return active
