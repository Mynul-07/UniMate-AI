from rest_framework import serializers
from .models import University, Program, Fee, Scholarship, HiddenCharge, Metric

class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = "__all__"

class ProgramSerializer(serializers.ModelSerializer):
    fees = FeeSerializer(many=True, read_only=True)
    class Meta:
        model = Program
        fields = ("id","name","degree_level","department","duration_semesters","fees")

class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = "__all__"

class HiddenChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiddenCharge
        fields = "__all__"

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = "__all__"

class UniversityListSerializer(serializers.ModelSerializer):
    reputation = serializers.SerializerMethodField()
    class Meta:
        model = University
        fields = ("id","name","city","type","website","reputation")
    def get_reputation(self, obj):
        return getattr(getattr(obj, "metrics", None), "reputation", None)

class UniversityDetailSerializer(serializers.ModelSerializer):
    metrics = MetricSerializer(read_only=True)
    class Meta:
        model = University
        fields = ("id","name","city","type","website","contact_email","contact_phone","transport_notes","metrics")
