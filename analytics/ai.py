from django.conf import settings
from tasks.models import Task

def get_ai_suggestions(user):
    suggestions = []
    
    # 1. Check for urgent tasks
    urgent_keywords = ['urgent', 'important', 'critical', 'asap']
    tasks = Task.objects.filter(status='pending')
    
    for task in tasks:
        # Priority Suggestion
        for keyword in urgent_keywords:
            if keyword in task.title.lower() or keyword in task.description.lower():
                if task.priority != 'high':
                    suggestions.append({
                        'task': task,
                        'reason': f"Contains keyword '{keyword}' - consider raising priority to High.",
                        'type': 'priority'
                    })
        
        # Deadline Helper
        if task.deadline:
            # Assuming tz aware
            pass 
            # If deadline is within 24h, mark as urgent suggestion
    
    return suggestions
