import os
import time
import json
import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, session
from werkzeug.utils import secure_filename
from utils.csv_handler import CSVHandler
from utils.claude_integration import ClaudeAnalyzer
from utils.memory_monitor import monitor_memory_usage, optimize_memory
from utils.db_connector import CSVData, AnalysisResult, db

from routes import main_bp

logger = logging.getLogger(__name__)

@main_bp.route('/')
def landing():
    """Render the assessment landing page explaining the purpose and instructions"""
    return render_template('assessment_landing.html')

@main_bp.route('/app')
def index():
    """Render the main application interface"""
    # Get recent CSV uploads
    try:
        recent_uploads = CSVData.query.order_by(CSVData.upload_date.desc()).limit(5).all()
    except Exception as e:
        # This is a deliberate error that candidates need to fix
        # Part of the assessment is identifying and fixing database connectivity issues
        logger.error(f"Database error when fetching recent uploads: {str(e)}")
        recent_uploads = []
    
    # Check if Claude integration is available
    claude = ClaudeAnalyzer()
    claude_available = claude.is_available()
    
    return render_template('index.html', 
                          recent_uploads=recent_uploads,
                          claude_available=claude_available)

@main_bp.route('/upload', methods=['POST'])
def upload_csv():
    """Handle CSV file upload and initial processing"""
    if 'csv_file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    
    file = request.files['csv_file']
    
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)
    
    if file and file.filename.endswith('.csv'):
        start_time = time.time()
        
        try:
            # Process the uploaded CSV file
            with monitor_memory_usage():
                csv_handler = CSVHandler(file)
                temp_path = csv_handler.save_file()
                df = csv_handler.load_csv()
                
                # Get file size
                file_size = os.path.getsize(temp_path) / 1024  # Size in KB
                
                # Create database record
                csv_data = CSVData(
                    filename=secure_filename(file.filename),
                    rows=csv_handler.metadata.get('rows', 0),
                    columns=csv_handler.metadata.get('columns', 0),
                    file_size=file_size,
                    column_names=json.dumps(csv_handler.metadata.get('column_names', [])),
                    status='processed'
                )
                db.session.add(csv_data)
                db.session.commit()
                
                # Store CSV data ID in session for later analysis
                session['csv_data_id'] = csv_data.id
                
                # Clean up temporary file
                csv_handler.cleanup()
                
                # Record processing time
                processing_time = time.time() - start_time
                
                # Redirect to analysis page
                flash(f'File uploaded and processed successfully in {processing_time:.2f} seconds', 'success')
                return redirect(url_for('main.analyze'))
                
        except Exception as e:
            logger.error(f"Error processing CSV upload: {str(e)}")
            flash(f'Error processing CSV file: {str(e)}', 'error')
            return redirect(url_for('main.index'))
    else:
        flash('Invalid file type. Please upload a CSV file', 'error')
        return redirect(url_for('main.index'))

@main_bp.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Analyze CSV data with Claude AI"""
    csv_data_id = session.get('csv_data_id')
    
    if not csv_data_id:
        flash('No CSV data found. Please upload a file first.', 'error')
        return redirect(url_for('main.index'))
    
    csv_data = CSVData.query.get(csv_data_id)
    
    if not csv_data:
        flash('CSV data not found', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # Handle analysis request
        analysis_type = request.form.get('analysis_type', 'summary')
        
        try:
            # Check if analysis already exists
            existing_analysis = AnalysisResult.query.filter_by(
                csv_data_id=csv_data_id, 
                analysis_type=analysis_type
            ).first()
            
            if existing_analysis:
                # Use existing analysis
                analysis_id = existing_analysis.id
                flash('Using existing analysis results', 'info')
            else:
                # Create new analysis
                start_time = time.time()
                
                # Load file data from CSV handler
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], csv_data.filename)
                csv_handler = CSVHandler()
                
                # For demo purposes, we'll generate a summary without loading the actual file
                column_names = json.loads(csv_data.column_names)
                data_description = {
                    "metadata": {
                        "rows": csv_data.rows,
                        "columns": csv_data.columns,
                        "column_names": column_names
                    },
                    "sample_data": [{"sample": "data"}],  # Placeholder
                    "column_descriptions": {
                        col: {"dtype": "unknown", "missing": 0, "unique_values": 0}
                        for col in column_names
                    }
                }
                
                # Call Claude for analysis
                claude = ClaudeAnalyzer()
                if claude.is_available():
                    analysis_result = claude.analyze_csv_data(data_description, analysis_type)
                    
                    # Save analysis result to database
                    result = AnalysisResult(
                        csv_data_id=csv_data_id,
                        analysis_type=analysis_type,
                        result=analysis_result.get('result', '')
                    )
                    db.session.add(result)
                    db.session.commit()
                    
                    analysis_id = result.id
                    
                    # Update CSV data status
                    csv_data.status = 'analyzed'
                    db.session.commit()
                    
                    processing_time = time.time() - start_time
                    flash(f'Analysis completed in {processing_time:.2f} seconds', 'success')
                else:
                    flash('Claude AI integration is not available. Please check API key configuration.', 'error')
                    return redirect(url_for('main.index'))
            
            # Redirect to results page
            return redirect(url_for('main.results', analysis_id=analysis_id))
            
        except Exception as e:
            logger.error(f"Error analyzing CSV data: {str(e)}")
            flash(f'Error analyzing CSV data: {str(e)}', 'error')
            return redirect(url_for('main.index'))
    
    # GET request - show analysis options
    return render_template('index.html', 
                          csv_data=csv_data,
                          show_analysis_options=True)

@main_bp.route('/results/<int:analysis_id>')
def results(analysis_id):
    """Display analysis results"""
    analysis = AnalysisResult.query.get(analysis_id)
    
    if not analysis:
        flash('Analysis results not found', 'error')
        return redirect(url_for('main.index'))
    
    csv_data = CSVData.query.get(analysis.csv_data_id)
    
    return render_template('results.html', 
                          analysis=analysis,
                          csv_data=csv_data)

@main_bp.route('/list')
def list_csvs():
    """List all uploaded CSV files"""
    csv_files = CSVData.query.order_by(CSVData.upload_date.desc()).all()
    return render_template('index.html', csv_files=csv_files, show_list=True)

@main_bp.route('/optimize_memory', methods=['POST'])
def optimize_app_memory():
    """Endpoint to manually trigger memory optimization"""
    saved = optimize_memory()
    return jsonify({
        'success': True,
        'message': f'Memory optimized, saved {saved:.2f}MB'
    })
