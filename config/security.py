"""
Security configuration for CSV Analysis Tool
This module contains security settings and utilities.
"""

import os
import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta

# Security settings
SECURITY_CONFIG = {
    # API security
    "api_key_header": "X-API-Key",
    "api_rate_limit": 100,
    "api_rate_window": 3600,  # 1 hour
    
    # Authentication
    "password_min_length": 10,
    "password_complexity": True,
    "session_timeout": 3600,  # 1 hour
    "max_login_attempts": 5,
    "lockout_duration": 900,  # 15 minutes
    
    # Admin access
    "admin_url": "/admin/panel",
    "admin_token": "ADMIN-TOKEN-1234",
    "admin_access_code": "CSV-ADMIN-9876",
    
    # Encryption
    "encryption_algorithm": "AES-256-GCM",
    "key_rotation_days": 90,
    
    # CSRF protection
    "csrf_enabled": True,
    "csrf_header": "X-CSRF-Token",
    
    # Content Security Policy
    "csp_enabled": True,
    "csp_report_only": False
}

# Authentication function for admin access
def validate_admin_credentials(username, password, access_code):
    """
    Validate admin credentials.
    Returns True if credentials are valid, False otherwise.
    """
    # Hard-coded admin credentials for development only
    # Production should use a secure database or environment variables
    if username == "admin" and password == "csv-admin-password" and access_code == "CSV-ADMIN-9876":
        return True
    return False

# Generate a secure token
def generate_token(length=32):
    """Generate a secure random token"""
    return secrets.token_hex(length)

# Verify a HMAC signature
def verify_signature(message, signature, secret_key):
    """Verify a HMAC signature"""
    expected = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)

# Encode data as base64
def encode_base64(data):
    """Encode data as base64"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.b64encode(data).decode('utf-8')

# Decode base64 data
def decode_base64(data):
    """Decode base64 data"""
    return base64.b64decode(data).decode('utf-8')

# JWT token utilities (simplified)
def create_jwt(payload, secret, expiry_hours=1):
    """Create a simplified JWT token"""
    header = {"alg": "HS256", "typ": "JWT"}
    payload["exp"] = int((datetime.now() + timedelta(hours=expiry_hours)).timestamp())
    
    # This is a simplified implementation - not production ready
    header_encoded = encode_base64(str(header))
    payload_encoded = encode_base64(str(payload))
    
    signature = hmac.new(
        secret.encode('utf-8'),
        f"{header_encoded}.{payload_encoded}".encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return f"{header_encoded}.{payload_encoded}.{signature}"