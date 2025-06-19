from faker import Faker
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

fake = Faker()

class ComplianceDataGenerator:
    def __init__(self):
        # Include ISO 27001 for completeness
        self.frameworks = ["SOC 2", "HIPAA", "GDPR", "PCI-DSS", "NIST", "ISO 27001"]
        self.providers = ["AWS", "Azure", "GCP"]
        self.severities = ["Critical", "High", "Medium", "Low"]
        self.control_descriptions = {
            "SOC 2": [
                "Quarterly access reviews", 
                "Formal code approvals", 
                "Vulnerability scans & remediation",
                "System monitoring controls",
                "Data backup procedures"
            ],
            "NIST": [
                "MFA on admin accounts", 
                "Database encryption at rest", 
                "Protection against malware",
                "Network segmentation",
                "Incident response procedures"
            ],
            "GDPR": [
                "Data subject rights", 
                "Data breach notification", 
                "Data protection impact assessments",
                "Consent management",
                "Data retention policies"
            ],
            "PCI-DSS": [
                "Cardholder data encryption", 
                "Access control", 
                "Network security",
                "Payment processing security",
                "Vulnerability management"
            ],
            "HIPAA": [
                "Encryption of PHI at rest", 
                "Access logging for ePHI", 
                "Periodic risk analysis",
                "Employee training",
                "Business associate agreements"
            ],
            "ISO 27001": [
                "Risk assessments", 
                "Information security policies", 
                "Incident management",
                "Asset management",
                "Supplier relationship security"
            ]
        }

    def generate_compliance_data(self, count: int = 50) -> List[Dict[str, Any]]:
        """
        Generate a list of mock compliance check records.
        Internally uses datetime for last_checked, but returns ISO strings when packaging for response.
        """
        data: List[Dict[str, Any]] = []
        now = datetime.now()
        
        for _ in range(count):
            framework = random.choice(self.frameworks)
            descriptions = self.control_descriptions.get(framework, ["General compliance check"])
            description = random.choice(descriptions)
            provider = random.choice(self.providers)
            severity = random.choice(self.severities)
            
            # Slightly different weights: Passing majority, Warning moderate, Failing fewer
            status = random.choices(["Passing", "Failing", "Warning"], weights=[0.7, 0.2, 0.1])[0]

            # Generate AI summary based on status
            if status == "Passing":
                summary = f"AI confirmed {description.lower()} requirements are met with {provider} configuration."
            elif status == "Warning":
                summary = f"AI detected potential issues with {description.lower()} that require attention."
            else:
                summary = f"AI detected non-compliance with {description.lower()} requirements on {provider}."

            # Generate last_checked as datetime between now and 30 days ago
            delta_days = random.randint(0, 30)
            delta_hours = random.randint(0, 23)
            delta_minutes = random.randint(0, 59)
            last_checked_dt = now - timedelta(days=delta_days, hours=delta_hours, minutes=delta_minutes)

            # Risk score should be higher for failing/critical items
            if status == "Failing" and severity == "Critical":
                risk_score = round(random.uniform(8.0, 10.0), 1)
            elif status == "Failing":
                risk_score = round(random.uniform(6.0, 9.0), 1)
            elif status == "Warning":
                risk_score = round(random.uniform(4.0, 7.0), 1)
            else:
                risk_score = round(random.uniform(1.0, 4.0), 1)

            data.append({
                "id": fake.uuid4(),
                "framework": framework,
                "provider": provider,
                "severity": severity,
                "status": status,
                "risk_score": risk_score,
                "description": description,
                "last_checked": last_checked_dt,  # store datetime internally
                "ai_summary": summary
            })
        return data

    def perform_scan(self, resources: List[str]) -> Dict[str, Any]:
        """
        Simulate a compliance scan over given resources.
        Returns a dict with scanned count, issues_found, and timestamp.
        """
        # Simulate finding issues in some percentage of resources
        issues_found = random.randint(0, max(1, len(resources) // 2))
        timestamp = datetime.now().isoformat()
        return {
            "scanned": len(resources),
            "issues_found": issues_found,
            "timestamp": timestamp
        }

    def generate_threat_data(self, count: int = 20) -> List[Dict[str, Any]]:
        """
        Generate threat data for compatibility with existing frontend
        """
        threat_types = [
            "DDoS Attack", "Malware", "Phishing", "Data Breach", 
            "Insider Threat", "Ransomware", "SQL Injection", "XSS Attack"
        ]
        sources = ["IDS", "SIEM", "Firewall", "Endpoint Protection", "Network Monitor"]
        
        threats = []
        now = datetime.now()
        
        for _ in range(count):
            threat_type = random.choice(threat_types)
            severity = random.choice(self.severities)
            source = random.choice(sources)
            
            # Generate realistic threat descriptions
            descriptions = {
                "DDoS Attack": "High volume of requests detected from multiple IP addresses",
                "Malware": "Suspicious file behavior detected on endpoint",
                "Phishing": "Suspicious email with malicious links detected",
                "Data Breach": "Unauthorized access attempt to sensitive data",
                "Insider Threat": "Unusual access pattern detected for privileged user",
                "Ransomware": "File encryption behavior detected on system",
                "SQL Injection": "Malicious SQL query attempt detected",
                "XSS Attack": "Cross-site scripting attempt detected"
            }
            
            delta_hours = random.randint(0, 72)
            timestamp = (now - timedelta(hours=delta_hours)).isoformat()
            
            threats.append({
                "id": fake.uuid4(),
                "threat_type": threat_type,
                "severity": severity,
                "description": descriptions.get(threat_type, "Security threat detected"),
                "timestamp": timestamp,
                "source": source
            })
            
        return threats

    def generate_budget_recommendations(self) -> List[Dict[str, Any]]:
        """
        Generate budget recommendations for compatibility with existing frontend
        """
        categories = [
            "Network Security", "Endpoint Protection", "Identity Management",
            "Cloud Security", "Security Training", "Incident Response",
            "Compliance Tools", "Threat Intelligence"
        ]
        
        recommendations = []
        
        for category in categories:
            current = round(random.uniform(50000, 500000), 2)
            # Some categories need increase, some decrease
            change_factor = random.uniform(0.8, 1.3)
            recommended = round(current * change_factor, 2)
            
            if recommended > current:
                reasoning = f"Increased threat activity requires additional investment in {category.lower()}"
                roi_impact = round(random.uniform(1.2, 2.5), 2)
            else:
                reasoning = f"Optimization opportunities identified in {category.lower()} spending"
                roi_impact = round(random.uniform(0.8, 1.1), 2)
            
            recommendations.append({
                "category": category,
                "current_allocation": current,
                "recommended_allocation": recommended,
                "reasoning": reasoning,
                "roi_impact": roi_impact
            })
            
        return recommendations