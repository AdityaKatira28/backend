from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class ComplianceCheck(BaseModel):
    id: str
    framework: str
    provider: str
    severity: str
    status: str
    risk_score: float
    description: str
    last_checked: str  # ISO string in responses
    ai_summary: str

class DashboardSummary(BaseModel):
    total_checks: int
    compliant: int
    non_compliant: int
    critical_count: int
    framework_scores: Dict[str, float]
    provider_stats: Dict[str, Dict[str, int]]
    recent_violations: List[ComplianceCheck]

class AiInsights(BaseModel):
    summary: Dict[str, Any]
    recommendations: List[Dict[str, str]]

class ScanRequest(BaseModel):
    resources: List[str]

class ScanResult(BaseModel):
    scanned: int
    issues_found: int
    timestamp: str  # ISO string

# Additional models for frontend compatibility
class ThreatData(BaseModel):
    """Model for threat data compatibility with existing frontend"""
    id: str
    threat_type: str
    severity: str
    description: str
    timestamp: str
    source: str

class BudgetRecommendation(BaseModel):
    """Model for budget recommendations compatibility"""
    category: str
    current_allocation: float
    recommended_allocation: float
    reasoning: str
    roi_impact: float

class HealthStatus(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    version: str