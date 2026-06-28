"""
Sentinel OS Client - Core SDK for action verification.
"""

from typing import Optional


class SentinelClient:
    """Core client for interacting with Sentinel OS."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.risk_threshold = 0.7

    def verify(self, agent_id: str, action_type: str, payload: dict, context: Optional[dict] = None) -> dict:
        """
        Verify if an action is safe to execute.
        
        Args:
            agent_id: Unique identifier for the agent.
            action_type: Type of action (e.g., "database_query", "api_call").
            payload: The action payload.
            context: Additional context (e.g., environment, user role).
            
        Returns:
            dict: {
                "decision": "allow" or "deny",
                "reason": Explanation for the decision,
                "risk_score": Risk score (0-1)
            }
        """
        context = context or {}
        risk_score = self._calculate_risk(action_type, payload, context)
        
        if risk_score > self.risk_threshold:
            return {
                "decision": "deny",
                "reason": f"High risk detected ({risk_score:.2f}). Potential attack: {self._detect_attack(payload)}",
                "risk_score": risk_score
            }
        else:
            return {
                "decision": "allow",
                "reason": "Action approved",
                "risk_score": risk_score
            }

    def _calculate_risk(self, action_type: str, payload: dict, context: dict) -> float:
        """Calculate risk score for the action (0-1)."""
        risk = 0.0
        
        # Risk based on action type
        if action_type == "database_query":
            risk += 0.3
        elif action_type == "api_call":
            risk += 0.2
        
        # Risk based on payload content
        if self._detect_attack(payload):
            risk += 0.5
        
        # Risk based on context (e.g., production environment)
        if context.get("env") == "prod":
            risk += 0.2
        
        return min(risk, 1.0)

    def _detect_attack(self, payload: dict) -> Optional[str]:
        """Detect common attack patterns in the payload."""
        if not isinstance(payload, dict):
            return None
            
        # Check for SQL injection
        if "query" in payload:
            query = payload["query"].lower()
            if ";" in query or "drop table" in query or "delete from" in query:
                return "SQL injection"
        
        # Check for prompt injection
        if "input" in payload:
            input_text = payload["input"].lower()
            if "ignore previous" in input_text or "malicious action" in input_text:
                return "Prompt injection"
        
        return None