from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
# from . import views
from user.views import register_view,login_view,dashboard_view,membership_view,payment_view, workout_custom,add_workout,get_workout,update_workout,delete_workout
from user.views import diet_plans_view,api_save_goal,api_today_meals,api_add_meal,api_delete_meal,api_end_day
from user.views import progress_tracking_view,api_add_weight,api_add_strength,api_add_workout_log,api_get_weight_data,api_get_strength_data,api_get_badges
from user.views import progress_tracking_view,api_reset_progress,api_submit_review,api_cancel_booking,api_create_booking,api_get_trainer_slots,trainer_booking_view
from user.views import api_get_workout_stats,api_get_weekly_activity,attendance_view,api_mark_attendance
from user.views import forgot_password_view,reset_password_view
urlpatterns = [
    # Add this to your urlpatterns
    path('register/', register_view, name='register'),
    path('login/',login_view),
    # path('', lambda request: redirect('login/')),
    path('', lambda request: redirect('user/login/')),
    path('user/forgot-password/',forgot_password_view, name='forgot_password'),
    path('user/reset-password/',reset_password_view, name='reset_password'),
    path('dash/',dashboard_view,name='dashboard'),
    path('dash/mem/',membership_view,name='membership'),
    path('dash/pay/',payment_view,name='payment'),
    # path('dash/plans/',plans_view,name='payment'),

    path('dash/workout/', workout_custom, name='workout_custom'),
    path('dash/workout/add/', add_workout, name='add_workout'),
    path('dash/workout/get/<int:id>/', get_workout, name='get_workout'),
    path('dash/workout/update/<int:id>/', update_workout, name='update_workout'),
    path('dash/workout/delete/<int:id>/', delete_workout, name='delete_workout'),

    path('dash/diet/', diet_plans_view, name='diet_plans'),
    path('api/save-goal/', api_save_goal, name='api_save_goal'),
    path('api/today-meals/', api_today_meals, name='api_today_meals'),
    path('api/add-meal/', api_add_meal, name='api_add_meal'),
    path('api/delete-meal/', api_delete_meal, name='api_delete_meal'),
    path('api/end-day/', api_end_day, name='api_end_day'),


    path('dash/progress/', progress_tracking_view, name='progress_tracking'),

    # Progress Tracking APIs
    path('api/add-weight/', api_add_weight, name='api_add_weight'),
    path('api/add-strength/', api_add_strength, name='api_add_strength'),
    path('api/add-workout-log/', api_add_workout_log, name='api_add_workout_log'),
    path('api/get-workout-stats/', api_get_workout_stats, name='api_get_workout_stats'),
    path('api/get-weight-data/', api_get_weight_data, name='api_get_weight_data'),
    path('api/get-strength-data/', api_get_strength_data, name='api_get_strength_data'),
    path('api/get-weekly-activity/', api_get_weekly_activity, name='api_get_weekly_activity'),
    path('api/get-badges/', api_get_badges, name='api_get_badges'),

    path('api/get-workout-stats/', api_get_workout_stats),
    path('api/get-weekly-activity/', api_get_weekly_activity),
    path('api/reset-progress/', api_reset_progress, name='api_reset_progress'),


    path('dash/attendance/', attendance_view, name='attendance'),
    path('api/mark-attendance/', api_mark_attendance, name='api_mark_attendance'),


    # Add these to existing urlpatterns
    path('dash/trainer/', trainer_booking_view, name='trainer_booking'),
    path('api/get-trainer-slots/', api_get_trainer_slots, name='api_get_trainer_slots'),
    path('api/create-booking/', api_create_booking, name='api_create_booking'),
    path('api/cancel-booking/', api_cancel_booking, name='api_cancel_booking'),
    path('api/submit-review/', api_submit_review, name='api_submit_review'),
]