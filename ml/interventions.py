def generate_interventions(student: dict, shap_factors: list) -> list:
    """
    Rule-based intervention generator.
    Returns a list of recommended actions for the student.
    """
    actions = []
    top_features = [f['feature'] for f in shap_factors]

    if student.get('absences', 0) > 10:
        actions.append({
            'type': 'attendance',
            'action': 'Schedule attendance review with student',
            'priority': 'high'
        })
    if student.get('failures', 0) >= 2:
        actions.append({
            'type': 'counselling',
            'action': 'Refer to academic counsellor immediately',
            'priority': 'high'
        })
    if student.get('studytime', 4) <= 2:
        actions.append({
            'type': 'study_plan',
            'action': 'Assign structured weekly study plan',
            'priority': 'medium'
        })
    if student.get('Dalc', 1) >= 3 or student.get('Walc', 1) >= 4:
        actions.append({
            'type': 'wellbeing',
            'action': 'Connect with school counsellor for wellbeing check',
            'priority': 'medium'
        })
    if 'absences' in top_features or 'failures' in top_features:
        actions.append({
            'type': 'extra_classes',
            'action': 'Enrol in extra support classes',
            'priority': 'medium'
        })
    if not actions:
        actions.append({
            'type': 'monitor',
            'action': 'Continue monitoring — check in next week',
            'priority': 'low'
        })
    return actions