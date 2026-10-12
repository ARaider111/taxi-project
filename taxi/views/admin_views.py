import openpyxl
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from taxi.models import User, Driver, Client, Shift, District, Street, Tariff, Order, AuditLog
from django.contrib.auth import logout
from django.db.models import Q, Sum, Count
from django.db import models
from django.utils import timezone
from taxi.utils import log_action 
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime, timedelta
from django.utils import timezone as tz
from .helpers import admin_required

@login_required
@admin_required
def admin_panel(request):
    return render(request, "admin_panel.html")














