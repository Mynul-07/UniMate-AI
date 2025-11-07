from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from .models import University, Program, Fee, Scholarship, HiddenCharge, Metric
from .serializers import (
    UniversityListSerializer, UniversityDetailSerializer, ProgramSerializer,
    ScholarshipSerializer, HiddenChargeSerializer, MetricSerializer
)

class UniversityListView(generics.ListAPIView):
    queryset = University.objects.all().order_by("name")
    serializer_class = UniversityListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        city = self.request.query_params.get("city")
        utype = self.request.query_params.get("type")
        search = self.request.query_params.get("search")
        if city:
            qs = qs.filter(city__icontains=city)
        if utype:
            qs = qs.filter(type__iexact=utype)
        if search:
            qs = qs.filter(name__icontains=search)
        return qs

class UniversityDetailView(generics.RetrieveAPIView):
    queryset = University.objects.all()
    serializer_class = UniversityDetailSerializer
    permission_classes = [permissions.AllowAny]

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def search_universities(request):
    q = request.query_params.get("q","")
    qs = University.objects.filter(Q(name__icontains=q))[:20]
    return Response([{"id": u.id, "name": u.name} for u in qs])

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def list_programs(request, pk):
    programs = Program.objects.filter(university_id=pk)
    return Response(ProgramSerializer(programs, many=True).data)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def list_fees(request, pk):
    programs = Program.objects.filter(university_id=pk).prefetch_related("fees")
    data = {"university_id": pk, "program_fees": []}
    for p in programs:
        for fee in p.fees.all():
            data["program_fees"].append({
                "program": p.name,
                "tuition_total": float(fee.tuition_total or 0),
                "admission_fee": float(fee.admission_fee or 0),
                "lab_fee": float(fee.lab_fee or 0),
                "other_fees": fee.other_fees,
                "currency": fee.currency,
            })
    return Response(data)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def list_scholarships(request, pk):
    sc = Scholarship.objects.filter(university_id=pk)
    return Response(ScholarshipSerializer(sc, many=True).data)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def list_hidden_charges(request, pk):
    hc = HiddenCharge.objects.filter(university_id=pk)
    return Response(HiddenChargeSerializer(hc, many=True).data)

class MetricListView(generics.ListCreateAPIView):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    permission_classes = [permissions.IsAdminUser]
