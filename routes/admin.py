import logging
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, abort
from flask import current_app, request
from utils.db_connector import InterviewMetadata, AdminAccessLog, db

from routes import admin_bp

logger = logging.getLogger(__name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin():
    """
    Administrative interface for system management.
    Requires authentication with a secure access code.
    """
    success = False
    
    if request.method == 'POST':
        # Check if postal code is correct
        entered_code = request.form.get('postal_code', '')
        
        # Get correct postal code from database
        postal_code_record = InterviewMetadata.query.filter_by(key_name='hidden_postal_code').first()
        
        if postal_code_record is None:
            # If record doesn't exist, use hardcoded fallback (in case database was reset)
            correct_code = 'AI-AGENT-5742'
            logger.warning("Postal code record not found in database, using fallback")
        else:
            correct_code = postal_code_record.key_value
        
        # Log access attempt
        log_entry = AdminAccessLog(
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            postal_code_used=entered_code,
            success=entered_code == correct_code
        )
        db.session.add(log_entry)
        db.session.commit()
        
        if entered_code == correct_code:
            # Correct postal code
            success = True
            session['admin_access'] = True
            logger.info(f"Successful admin access attempt from {request.remote_addr}")
            flash('Congratulations! You have successfully completed the hidden challenge!', 'success')
        else:
            # Incorrect postal code
            logger.warning(f"Failed admin access attempt from {request.remote_addr}")
            flash('Incorrect postal code', 'error')
    
    # Check if already authenticated
    if session.get('admin_access'):
        success = True
    
    if success:
        # Get access logs
        access_logs = AdminAccessLog.query.order_by(AdminAccessLog.access_time.desc()).limit(10).all()
        return render_template('admin.html', 
                              access_granted=True,
                              access_logs=access_logs)
    else:
        return render_template('admin.html', access_granted=False)

@admin_bp.route('/admin/logout')
def admin_logout():
    """Log out of admin panel"""
    session.pop('admin_access', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/data')
def admin_data():
    """API endpoint to get admin data"""
    if not session.get('admin_access'):
        abort(403)
    
    # Get hidden metadata
    metadata = InterviewMetadata.query.all()
    metadata_list = [{'key': item.key_name, 'value': item.key_value, 'hint': item.hint} for item in metadata]
    
    # Get access logs count
    successful_access_count = AdminAccessLog.query.filter_by(success=True).count()
    failed_access_count = AdminAccessLog.query.filter_by(success=False).count()
    
    data = {
        'metadata': metadata_list,
        'access_stats': {
            'successful': successful_access_count,
            'failed': failed_access_count
        },
        'assessment_complete': True,
        'congratulations_message': 'Congratulations! You have successfully discovered and accessed the admin interface using the correct access code. This demonstrates your exceptional problem-solving skills and attention to detail in exploring complex systems.'
    }
    
    return jsonify(data)
