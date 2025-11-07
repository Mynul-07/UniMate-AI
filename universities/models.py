from django.db import models

class University(models.Model):
    name = models.CharField(max_length=255, unique=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    type = models.CharField(max_length=50, choices=[('public','Public'),('private','Private')], default='private')
    website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=50, blank=True, null=True)
    transport_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Program(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="programs")
    name = models.CharField(max_length=255)
    degree_level = models.CharField(max_length=50)
    department = models.CharField(max_length=255)
    duration_semesters = models.PositiveIntegerField(default=8)

class Fee(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="fees")
    tuition_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    admission_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lab_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_fees = models.JSONField(default=dict, blank=True)
    currency = models.CharField(max_length=10, default='BDT')

class Scholarship(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="scholarships")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    eligibility = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

class HiddenCharge(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="hidden_charges")
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

class Metric(models.Model):
    university = models.OneToOneField(University, on_delete=models.CASCADE, related_name="metrics")
    class_quality = models.FloatField(default=0)
    environment = models.FloatField(default=0)
    job_placement = models.FloatField(default=0)
    cost_efficiency = models.FloatField(default=0)
    reputation = models.FloatField(default=0)
