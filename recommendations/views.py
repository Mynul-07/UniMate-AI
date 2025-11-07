from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from universities.models import University, Metric

def rank_universities(priorities):
    # naive example: average the selected metrics
    weights = {
        "Class Quality": "class_quality",
        "Environment": "environment",
        "Job Placement": "job_placement",
        "Cost Efficiency": "cost_efficiency",
        "Reputation": "reputation",
    }
    selected = [weights[p] for p in priorities if p in weights]
    results = []
    for uni in University.objects.all().select_related("metrics"):
        m = getattr(uni, "metrics", None)
        if not m or not selected:
            score = 0.0
        else:
            vals = [getattr(m, key) for key in selected]
            score = sum(vals) / len(vals)
        results.append({"university_name": uni.name, "city": uni.city, "overall_score": round(float(score), 2)})
    results.sort(key=lambda x: x["overall_score"], reverse=True)
    return results

class UniversityRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        budget = request.data.get("budget")
        location = request.data.get("location")
        priorities = request.data.get("priority", [])
        if budget is None or not location:
            return Response({"detail": "Budget or location missing."}, status=400)
        ranked = rank_universities(priorities)[:10]
        return Response({"criteria_used": priorities, "results": ranked})

class SubjectRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        ssc = request.data.get("ssc_gpa")
        hsc = request.data.get("hsc_gpa")
        if ssc is None or hsc is None:
            return Response({"detail": "Insufficient data to generate suggestions — please provide SSC and HSC results."}, status=422)
        # Minimal placeholder results
        return Response({
            "suggestions": [
                {"subject": "Computer Science & Engineering", "university": "Example University", "match_score": 0.85, "reason": "Strong labs"},
                {"subject": "BBA (Business Administration)", "university": "Example University", "match_score": 0.78, "reason": "Good placement"}
            ],
            "explanation": "Prototype ranking by simple rules."
        })

class HistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response({"history": []})
