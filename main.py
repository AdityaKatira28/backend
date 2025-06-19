from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from datetime import datetime
import uvicorn
import os

# Import models and utilities
from models import (
    DashboardSummary, ComplianceCheck, AiInsights, ScanRequest, ScanResult,
    ThreatData, BudgetRecommendation, HealthStatus
)
from utils import ComplianceDataGenerator

# Create FastAPI app
app = FastAPI(
    title="GRC Compliance Monitoring API",
    description="AI-powered compliance monitoring system for cloud infrastructure",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize data generator and create mock data
generator = ComplianceDataGenerator()
_compliance_data_internal = generator.generate_compliance_data(50)
_threat_data = generator.generate_threat_data(20)
_budget_recommendations = generator.generate_budget_recommendations()

def _serialize_record(record: dict) -> dict:
    """
    Convert internal record with datetime to dict with ISO string for Pydantic.
    """
    serialized = record.copy()
    lc = serialized.get("last_checked")
    if isinstance(lc, datetime):
        serialized["last_checked"] = lc.isoformat()
    else:
        serialized["last_checked"] = str(lc)
    return serialized

@app.get("/")
def root():
    """Root endpoint with basic info."""
    return {
        "message": "GRC Compliance Monitoring API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", response_model=HealthStatus)
def health_check():
    """Health check endpoint."""
    return HealthStatus(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.get("/api/test")
def api_test():
    """API connectivity test endpoint for frontend integration."""
    return {
        "message": "Backend API connection successful",
        "status": "connected",
        "timestamp": datetime.now().isoformat(),
        "api_version": "1.0.0",
        "available_endpoints": [
            "/api/test",
            "/api/checks", 
            "/health",
            "/docs"
        ]
    }

@app.get("/api/checks", response_model=List[ComplianceCheck])
def get_compliance_checks(
    status: Optional[str] = Query(None, description="Filter by status: Passing, Failing, Warning"),
    severity: Optional[str] = Query(None, description="Filter by severity: Critical, High, Medium, Low"),
    framework: Optional[str] = Query(None, description="Filter by framework: SOC 2, HIPAA, GDPR, PCI-DSS, NIST, ISO 27001"),
    provider: Optional[str] = Query(None, description="Filter by provider: AWS, Azure, GCP")
):
    """
    Return list of compliance checks, optionally filtered by status, severity, framework, and/or provider.
    Case-insensitive filtering.
    """
    filtered_internal = list(_compliance_data_internal)
    
    if status:
        status_lower = status.lower()
        filtered_internal = [
            rec for rec in filtered_internal
            if isinstance(rec.get("status"), str) and rec["status"].lower() == status_lower
        ]
    
    if severity:
        severity_lower = severity.lower()
        filtered_internal = [
            rec for rec in filtered_internal
            if isinstance(rec.get("severity"), str) and rec["severity"].lower() == severity_lower
        ]
    
    if framework:
        framework_lower = framework.lower()
        filtered_internal = [
            rec for rec in filtered_internal
            if isinstance(rec.get("framework"), str) and rec["framework"].lower() == framework_lower
        ]
    
    if provider:
        provider_lower = provider.lower()
        filtered_internal = [
            rec for rec in filtered_internal
            if isinstance(rec.get("provider"), str) and rec["provider"].lower() == provider_lower
        ]
    
    # Serialize each record for Pydantic
    serialized = [_serialize_record(rec) for rec in filtered_internal]
    return [ComplianceCheck(**item) for item in serialized]

@app.get("/api/dashboard", response_model=DashboardSummary)
def get_dashboard_summary():
    """
    Return aggregated compliance statistics.
    """
    data = _compliance_data_internal

    compliant = [rec for rec in data if rec.get("status") == "Passing"]
    non_compliant = [rec for rec in data if rec.get("status") != "Passing"]

    # Framework scores: % Passing among all checks of that framework
    framework_scores: Dict[str, float] = {}
    for fw in generator.frameworks:
        checks_fw = [rec for rec in data if rec.get("framework") == fw]
        if checks_fw:
            passing_count = sum(1 for rec in checks_fw if rec.get("status") == "Passing")
            score = round((passing_count / len(checks_fw)) * 100, 1)
            framework_scores[fw] = score

    # Provider stats
    provider_stats: Dict[str, Dict[str, int]] = {}
    for prov in generator.providers:
        checks_prov = [rec for rec in data if rec.get("provider") == prov]
        total = len(checks_prov)
        compliant_count = sum(1 for rec in checks_prov if rec.get("status") == "Passing")
        critical_fails = sum(1 for rec in checks_prov if rec.get("severity") == "Critical" and rec.get("status") != "Passing")
        provider_stats[prov] = {
            "total": total,
            "compliant": compliant_count,
            "critical": critical_fails
        }

    # Recent violations: non-compliant sorted by last_checked desc
    recent_violations_internal = non_compliant.copy()
    recent_violations_internal.sort(
        key=lambda rec: rec.get("last_checked") if isinstance(rec.get("last_checked"), datetime) else datetime.min,
        reverse=True
    )
    # Serialize top 5
    recent_serialized = [_serialize_record(rec) for rec in recent_violations_internal[:5]]
    recent_objs = [ComplianceCheck(**item) for item in recent_serialized]

    dashboard = DashboardSummary(
        total_checks=len(data),
        compliant=len(compliant),
        non_compliant=len(non_compliant),
        critical_count=sum(1 for rec in non_compliant if rec.get("severity") == "Critical"),
        framework_scores=framework_scores,
        provider_stats=provider_stats,
        recent_violations=recent_objs
    )
    return dashboard

@app.get("/api/ai-insights", response_model=AiInsights)
def get_ai_insights():
    """
    Return AI-driven insights and recommendations.
    """
    data = _compliance_data_internal
    non_compliant = [rec for rec in data if rec.get("status") != "Passing"]
    total = len(data)
    passing_count = sum(1 for rec in data if rec.get("status") == "Passing")

    critical_violations = sum(1 for rec in non_compliant if rec.get("severity") == "Critical")

    # Count failures by description
    failure_counts: Dict[str, int] = {}
    for rec in non_compliant:
        desc = rec.get("description", "Unknown")
        failure_counts[desc] = failure_counts.get(desc, 0) + 1
    most_common_failure = max(failure_counts, key=failure_counts.get) if failure_counts else None

    # Count failures by provider
    provider_fails: Dict[str, int] = {}
    for prov in generator.providers:
        count = sum(1 for rec in non_compliant if rec.get("provider") == prov)
        provider_fails[prov] = count
    most_problematic_provider = max(provider_fails, key=provider_fails.get) if provider_fails and max(provider_fails.values()) > 0 else None

    # Overall compliance percentage
    overall_compliance_percentage = round((passing_count / total) * 100, 1) if total > 0 else None

    # Build summary dict
    summary: Dict[str, Any] = {
        "critical_violations": critical_violations,
        "overall_compliance_percentage": overall_compliance_percentage,
        "total_non_compliant": len(non_compliant)
    }
    if most_common_failure:
        summary["most_common_failure"] = most_common_failure
    else:
        summary["most_common_failure"] = None
    if most_problematic_provider:
        summary["most_problematic_provider"] = most_problematic_provider
    else:
        summary["most_problematic_provider"] = None

    # Build recommendations list conditionally
    recommendations: List[Dict[str, str]] = []
    if critical_violations > 0:
        recommendations.append({
            "priority": "Critical",
            "title": "Address Critical Violations",
            "description": f"There are {critical_violations} critical violations requiring immediate attention.",
            "action": "Prioritize remediation of critical severity issues immediately."
        })
    if most_common_failure:
        recommendations.append({
            "priority": "High",
            "title": "Investigate Common Failure Pattern",
            "description": f"The most common failure is '{most_common_failure}' with {failure_counts[most_common_failure]} occurrences.",
            "action": "Develop automated remediation or additional monitoring for this control."
        })
    if most_problematic_provider:
        count_pf = provider_fails.get(most_problematic_provider, 0)
        if count_pf > 0:
            recommendations.append({
                "priority": "Medium",
                "title": "Review Provider Configuration",
                "description": f"{most_problematic_provider} has {count_pf} compliance failures.",
                "action": "Conduct a comprehensive security audit of resources in this cloud provider."
            })

    return AiInsights(summary=summary, recommendations=recommendations)

@app.post("/api/scan", response_model=ScanResult)
def initiate_compliance_scan(request: ScanRequest):
    """
    Initiate a new compliance scan on provided resources.
    """
    if not request.resources:
        raise HTTPException(status_code=400, detail="No resources provided for scanning")
    result = generator.perform_scan(request.resources)
    return ScanResult(
        scanned=result["scanned"],
        issues_found=result["issues_found"],
        timestamp=result["timestamp"]
    )

@app.get("/api/threats", response_model=List[ThreatData])
def get_threats(
    severity: Optional[str] = Query(None, description="Filter by severity"),
    threat_type: Optional[str] = Query(None, description="Filter by threat type")
):
    """
    Get threat data for frontend compatibility
    """
    filtered_threats = _threat_data.copy()
    
    if severity:
        severity_lower = severity.lower()
        filtered_threats = [
            threat for threat in filtered_threats
            if threat.get("severity", "").lower() == severity_lower
        ]
    
    if threat_type:
        threat_type_lower = threat_type.lower()
        filtered_threats = [
            threat for threat in filtered_threats
            if threat.get("threat_type", "").lower() == threat_type_lower
        ]
    
    return [ThreatData(**threat) for threat in filtered_threats]

@app.get("/api/budget-recommendations", response_model=List[BudgetRecommendation])
def get_budget_recommendations():
    """
    Get budget recommendations for frontend compatibility
    """
    return [BudgetRecommendation(**rec) for rec in _budget_recommendations]

@app.get("/api/stats")
def get_system_stats():
    """
    Get system statistics for dashboard
    """
    data = _compliance_data_internal
    threats = _threat_data
    
    # Calculate stats
    total_checks = len(data)
    compliant_checks = sum(1 for rec in data if rec.get("status") == "Passing")
    compliance_percentage = round((compliant_checks / total_checks) * 100, 1) if total_checks > 0 else 0
    
    critical_threats = sum(1 for threat in threats if threat.get("severity") == "Critical")
    high_threats = sum(1 for threat in threats if threat.get("severity") == "High")
    
    return {
        "total_checks": total_checks,
        "compliant_checks": compliant_checks,
        "compliance_percentage": compliance_percentage,
        "total_threats": len(threats),
        "critical_threats": critical_threats,
        "high_threats": high_threats,
        "last_updated": datetime.now().isoformat()
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting GRC Compliance Monitoring API on port {port}")
    print(f"📚 API Documentation: http://localhost:{port}/docs")
    print(f"🏥 Health Check: http://localhost:{port}/health")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

