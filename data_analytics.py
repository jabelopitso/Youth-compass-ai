# Data Analytics for Long-Term Impact Measurement
import json
from datetime import datetime, timedelta
from collections import defaultdict

class ImpactAnalytics:
    """Analytics engine to measure long-term development impact"""
    
    def __init__(self):
        # Simulated data - in production this would connect to a database
        self.user_outcomes = {
            'total_users': 15420,
            'successful_placements': 8934,
            'pathway_success_rates': {
                'digital': {'users': 6200, 'employed': 4030, 'rate': 65},
                'green': {'users': 4100, 'employed': 2255, 'rate': 55},
                'entrepreneurship': {'users': 5120, 'employed': 3584, 'rate': 70}
            },
            'geographic_distribution': {
                'Gauteng': 4500,
                'Western Cape': 3200,
                'KwaZulu-Natal': 2800,
                'Eastern Cape': 2100,
                'Other': 2820
            },
            'skills_development_impact': {
                'digital_literacy': 12300,
                'problem_solving': 9800,
                'communication': 11200,
                'entrepreneurship': 7600
            }
        }
    
    def calculate_economic_impact(self):
        """Calculate the economic impact of the platform"""
        avg_salary_increase = 3500  # Average monthly salary increase
        employed_users = self.user_outcomes['successful_placements']
        
        monthly_impact = employed_users * avg_salary_increase
        annual_impact = monthly_impact * 12
        
        return {
            'monthly_economic_impact': monthly_impact,
            'annual_economic_impact': annual_impact,
            'users_lifted_from_unemployment': employed_users,
            'average_salary_increase': avg_salary_increase
        }
    
    def get_pathway_optimization_data(self):
        """Provide data for pathway optimization"""
        pathways = self.user_outcomes['pathway_success_rates']
        
        optimization_insights = []
        for pathway, data in pathways.items():
            success_rate = data['rate']
            if success_rate < 60:
                optimization_insights.append({
                    'pathway': pathway,
                    'current_rate': success_rate,
                    'recommendation': 'Needs improvement - review course recommendations',
                    'priority': 'High'
                })
            elif success_rate < 70:
                optimization_insights.append({
                    'pathway': pathway,
                    'current_rate': success_rate,
                    'recommendation': 'Good performance - minor optimizations needed',
                    'priority': 'Medium'
                })
            else:
                optimization_insights.append({
                    'pathway': pathway,
                    'current_rate': success_rate,
                    'recommendation': 'Excellent performance - use as model for others',
                    'priority': 'Low'
                })
        
        return optimization_insights
    
    def generate_impact_report(self):
        """Generate comprehensive impact report"""
        economic_impact = self.calculate_economic_impact()
        optimization_data = self.get_pathway_optimization_data()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_users_served': self.user_outcomes['total_users'],
                'successful_job_placements': self.user_outcomes['successful_placements'],
                'overall_success_rate': round((self.user_outcomes['successful_placements'] / self.user_outcomes['total_users']) * 100, 1),
                'economic_impact_annual': economic_impact['annual_economic_impact']
            },
            'pathway_performance': self.user_outcomes['pathway_success_rates'],
            'geographic_reach': self.user_outcomes['geographic_distribution'],
            'skills_development': self.user_outcomes['skills_development_impact'],
            'optimization_recommendations': optimization_data,
            'long_term_projections': {
                'projected_users_next_year': self.user_outcomes['total_users'] * 2.5,
                'projected_economic_impact': economic_impact['annual_economic_impact'] * 2.5,
                'sustainability_score': 85  # Based on self-improving AI and community networks
            }
        }
        
        return report
    
    def update_success_metrics(self, pathway, success=True):
        """Update success metrics when user provides feedback"""
        pathway_data = self.user_outcomes['pathway_success_rates'][pathway]
        
        if success:
            pathway_data['employed'] += 1
        
        pathway_data['users'] += 1
        pathway_data['rate'] = round((pathway_data['employed'] / pathway_data['users']) * 100)
        
        return pathway_data['rate']

class SelfImprovingSystem:
    """System that learns and improves from user interactions"""
    
    def __init__(self):
        self.learning_data = {
            'successful_pathways': defaultdict(list),
            'failed_pathways': defaultdict(list),
            'user_feedback_patterns': defaultdict(int),
            'course_effectiveness': defaultdict(dict)
        }
    
    def learn_from_feedback(self, user_profile, pathway, outcome, feedback_data):
        """Learn from user feedback to improve future recommendations"""
        learning_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_skills': user_profile.get('skills_profile', {}),
            'pathway_chosen': pathway,
            'outcome': outcome,  # 'success', 'partial', 'failure'
            'feedback': feedback_data
        }
        
        if outcome == 'success':
            self.learning_data['successful_pathways'][pathway].append(learning_entry)
        else:
            self.learning_data['failed_pathways'][pathway].append(learning_entry)
        
        # Update feedback patterns
        self.learning_data['user_feedback_patterns'][f"{pathway}_{outcome}"] += 1
    
    def get_improved_recommendations(self, user_profile):
        """Generate improved recommendations based on learning data"""
        # Analyze successful patterns
        recommendations = []
        
        for pathway, successes in self.learning_data['successful_pathways'].items():
            if len(successes) > 10:  # Enough data points
                success_rate = len(successes) / (len(successes) + len(self.learning_data['failed_pathways'][pathway]))
                
                if success_rate > 0.7:  # High success rate
                    recommendations.append({
                        'pathway': pathway,
                        'confidence': success_rate,
                        'reason': f'High success rate ({success_rate:.1%}) based on {len(successes)} successful cases'
                    })
        
        return sorted(recommendations, key=lambda x: x['confidence'], reverse=True)

# Usage example:
# analytics = ImpactAnalytics()
# report = analytics.generate_impact_report()
# print(f"Platform has helped {report['summary']['successful_job_placements']} youth find employment")