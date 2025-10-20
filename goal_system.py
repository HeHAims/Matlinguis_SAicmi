# core/goal_system.py

class GoalSystem:
    def __init__(self):
        self.goals = []
        self.active_goal = None
    
    def add_goal(self, goal, priority=0.5):
        self.goals.append((goal, priority))
        self.goals.sort(key=lambda x: x[1], reverse=True)  # Sort by priority
        if not self.active_goal:
            self.active_goal = goal
    
    def get_active_goal(self):
        return self.active_goal
    
    def complete_goal(self, goal):
        self.goals = [(g, p) for g, p in self.goals if g != goal]
        if self.goals:
            self.active_goal = self.goals[0][0]
        else:
            self.active_goal = None
    
    def pursue(self):
        if self.active_goal:
            return f"Working on: {self.active_goal}"
        return "No active goals"