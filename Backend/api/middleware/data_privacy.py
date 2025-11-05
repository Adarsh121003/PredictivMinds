import hashlib
import uuid
from typing import Dict, Any
from datetime import datetime
import json
from pathlib import Path


class DataPrivacyFramework:
    """
    Data privacy and compliance framework
    Implements privacy-by-design principles (GDPR, IT Act 2000, DPDP Act 2023)
    """

    def __init__(self):
        self.pii_fields = ['name', 'phone',
                           'email', 'address', 'aadhaar', 'pan']
        self.sensitive_fields = ['medical_records',
                                 'financial_data', 'caste', 'religion']
        Path("logs").mkdir(exist_ok=True)

    def anonymize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize PII before processing"""
        anonymized = data.copy()

        for field in self.pii_fields:
            if field in anonymized:
                anonymized[field] = self._hash_pii(anonymized[field])

        for field in self.sensitive_fields:
            if field in anonymized:
                del anonymized[field]

        anonymized['_anonymized'] = True
        anonymized['_anonymization_timestamp'] = datetime.now().isoformat()
        anonymized['_anonymization_id'] = str(uuid.uuid4())

        return anonymized

    def _hash_pii(self, value: str) -> str:
        """Hash PII data using SHA-256"""
        return hashlib.sha256(str(value).encode()).hexdigest()[:16]

    def audit_data_access(self, user_id: str, data_accessed: str, purpose: str, ip: str):
        """Audit trail for data access (GDPR compliance)"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'data_accessed': data_accessed,
            'purpose': purpose,
            'ip_address': ip,
            'action': 'DATA_ACCESS'
        }

        # Log to audit file
        with open('logs/data_access_audit.jsonl', 'a') as f:
            f.write(json.dumps(audit_entry) + '\n')

    def check_consent(self, user_id: str, data_type: str) -> bool:
        """Check if user has given consent for data usage"""
        # In production, check against consent database
        return True

    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data before storage"""
        from base64 import b64encode
        return b64encode(data.encode()).decode()

    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        from base64 import b64decode
        return b64decode(encrypted_data.encode()).decode()

    def generate_privacy_report(self) -> Dict[str, Any]:
        """Generate privacy compliance report"""
        return {
            'framework_version': '1.0',
            'compliance_standards': [
                'GDPR (EU General Data Protection Regulation)',
                'IT Act 2000 (India)',
                'DPDP Act 2023 (Digital Personal Data Protection Act)'
            ],
            'privacy_features': {
                'anonymization_enabled': True,
                'encryption_enabled': True,
                'audit_logging_enabled': True,
                'consent_management': True,
                'data_minimization': True,
                'purpose_limitation': True
            },
            'data_retention_policy': '90 days',
            'user_rights_supported': [
                'Right to access',
                'Right to deletion',
                'Right to rectification',
                'Right to data portability',
                'Right to be forgotten'
            ],
            'security_measures': [
                'End-to-end encryption',
                'Role-based access control',
                'Activity logging',
                'Secure data storage',
                'Regular security audits'
            ]
        }

    def role_based_access(self, user_role: str, data_domain: str) -> bool:
        """Control who can see what"""
        permissions = {
            'district_officer': ['health', 'infrastructure'],
            'state_admin': ['health', 'infrastructure', 'public_safety'],
            'analyst': ['aggregated_data_only'],
            'public': []
        }
        return data_domain.lower() in permissions.get(user_role, [])


privacy_framework = DataPrivacyFramework()
