"""
Administrative panel for CSV Analysis Tool.
This module handles admin functionality for the application.
"""

import logging
import json
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from flask import request, jsonify, session, current_app, abort

# Create the admin blueprint for the admin panel routes
admin_panel_bp = Blueprint('admin_panel', __name__, url_prefix='/admin')

logger = logging.getLogger(__name__)

# Security configuration for admin access
ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "csv-admin-password",
    "token": "ADMIN-TOKEN-1234",
    "access_code": "CSV-ADMIN-9876"
}

@admin_panel_bp.route('/panel', methods=['GET', 'POST'])
def admin_panel():
    """
    Main administrative interface for the CSV Analysis Tool.
    Handles authentication and displays admin dashboard.
    """
    authenticated = False
    
    if session.get('admin_authenticated'):
        authenticated = True
    
    if request.method == 'POST':
        # Handle authentication
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        access_code = request.form.get('access_code', '')
        
        if (username == ADMIN_CREDENTIALS['username'] and 
            password == ADMIN_CREDENTIALS['password'] and 
            access_code == ADMIN_CREDENTIALS['access_code']):
            # Successful authentication
            session['admin_authenticated'] = True
            authenticated = True
            flash('Admin authentication successful', 'success')
        else:
            # Failed authentication
            flash('Invalid credentials', 'error')
    
    if authenticated:
        # Display admin dashboard
        return render_template('admin.html', 
                              is_admin_panel=True, 
                              system_status="Operational",
                              user_count=1250,
                              csv_files_processed=427,
                              system_version="1.0.4")
    else:
        # Show login form
        return render_template('admin_login.html')

@admin_panel_bp.route('/panel/logout')
def admin_logout():
    """Log out of admin panel"""
    session.pop('admin_authenticated', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('admin_panel.admin_panel'))

@admin_panel_bp.route('/panel/users')
def admin_users():
    """User management in admin panel"""
    if not session.get('admin_authenticated'):
        flash('Authentication required', 'error')
        return redirect(url_for('admin_panel.admin_panel'))
    
    # This would normally query the database
    mock_users = [
        {"id": 1, "username": "user1", "last_login": "2025-05-10 14:22:15"},
        {"id": 2, "username": "user2", "last_login": "2025-05-11 09:45:32"},
        {"id": 3, "username": "user3", "last_login": "2025-05-12 11:17:08"}
    ]
    
    return render_template('admin_users.html', users=mock_users)

@admin_panel_bp.route('/panel/settings')
def admin_settings():
    """System settings in admin panel"""
    if not session.get('admin_authenticated'):
        flash('Authentication required', 'error')
        return redirect(url_for('admin_panel.admin_panel'))
    
    # Mock settings
    mock_settings = {
        "app_name": "CSV Analysis Tool",
        "version": "1.0.4",
        "max_upload_size": "16MB",
        "debug_mode": False,
        "log_level": "INFO",
        "maintenance_mode": False
    }
    
    return render_template('admin_settings.html', settings=mock_settings)

@admin_panel_bp.route('/panel/api/status')
def api_status():
    """API endpoint for system status"""
    if not session.get('admin_authenticated'):
        abort(403)
    
    status_data = {
        "status": "operational",
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "version": "1.0.4",
        "database": "connected",
        "cache": "active",
        "services": [
            {"name": "web", "status": "online"},
            {"name": "api", "status": "online"},
            {"name": "worker", "status": "online"},
            {"name": "scheduler", "status": "online"}
        ]
    }
    
    return jsonify(status_data)