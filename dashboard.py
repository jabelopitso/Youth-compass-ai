# Admin Dashboard for Impact Monitoring
from flask import Blueprint, render_template, jsonify
from data_analytics import ImpactAnalytics, SelfImprovingSystem

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/admin')

analytics = ImpactAnalytics()
learning_system = SelfImprovingSystem()

@dashboard_bp.route('/')
def admin_dashboard():
    """Main admin dashboard showing impact metrics"""
    impact_report = analytics.generate_impact_report()
    return render_template('admin/dashboard.html', report=impact_report)

@dashboard_bp.route('/api/impact-data')
def get_impact_data():
    """API endpoint for real-time impact data"""
    return jsonify(analytics.generate_impact_report())

@dashboard_bp.route('/api/pathway-performance')
def get_pathway_performance():
    """API endpoint for pathway performance data"""
    return jsonify(analytics.get_pathway_optimization_data())

# Register blueprint in main app
def register_dashboard(app):
    app.register_blueprint(dashboard_bp)