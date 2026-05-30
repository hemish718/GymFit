from django.shortcuts import render, redirect
from django.contrib import messages
# from .models import LoginUser


from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password  # For password hashing
from .models import Users
import re

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        errors = []
        
        # Check if all fields are filled
        if not name or not email or not password:
            errors.append("Name, Email and Password are required")
        
        # Check password match
        if password != confirm_password:
            errors.append("Passwords do not match")
        
        # Check password length
        if len(password) < 4:
            errors.append("Password must be at least 4 characters")
        
        # Check if email already exists
        if Users.objects.filter(email=email).exists():
            errors.append("Email already registered. Please login.")
        
        # Check phone format (optional)
        if phone and not phone.isdigit():
            errors.append("Phone number should contain only digits")
        
        if phone and len(phone) != 10:
            errors.append("Phone number should be 10 digits")
        
        # Check email format
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors.append("Invalid email format")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'user/register.html')
        
        # Create new user
        try:
            user = Users.objects.create(
                name=name,
                email=email,
                phone=phone if phone else None,
                password=password  # Store password (you can hash it if needed)
            )
            messages.success(request, f"Registration successful! Welcome {name}. Please login.")
            return redirect('/user/login/')
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return render(request, 'user/register.html')
    
    return render(request, 'user/register.html')

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Users
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Users
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Users
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Users

def login_view(request):
    # Clear old messages
    storage = messages.get_messages(request)
    storage.used = True
    
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        print(f"🔍 Login attempt - Username: {username}")  # 🔥 Debug

        if not username or not password:
            messages.error(request, "Please enter both email/name and password.")
            return render(request, "user/login.html")

        # Find user by email or name
        user = None
        if Users.objects.filter(email=username).exists():
            user = Users.objects.get(email=username)
            print(f"✅ User found by email: {user.name}")  # 🔥 Debug
        elif Users.objects.filter(name=username).exists():
            user = Users.objects.get(name=username)
            print(f"✅ User found by name: {user.name}")  # 🔥 Debug

        if not user:
            print("❌ User not found")  # 🔥 Debug
            messages.error(request, "User not found. Please register first.")
            return render(request, "user/login.html")

        print(f"🔐 Password check - DB: {user.password}, Input: {password}")  # 🔥 Debug

        if user.password == password:
            # Set session
            request.session['user_id'] = user.user_id
            request.session['user_name'] = user.name
            request.session['user_email'] = user.email
            
            print(f"✅ Session set - user_id: {user.user_id}")  # 🔥 Debug
            print(f"✅ Session keys: {request.session.keys()}")  # 🔥 Debug
            
            messages.success(request, f"Welcome back, {user.name}! 🎉")
            
            # 🔥 TRY BOTH REDIRECTS
            try:
                return redirect("/user/dash/")
            except:
                return redirect("/user/dash")
        else:
            print("❌ Password mismatch")  # 🔥 Debug
            messages.error(request, "Invalid Password. Please try again.")
            return render(request, "user/login.html")

    return render(request, "user/login.html")


from django.shortcuts import render, redirect
from .models import Users, Memberships, MembershipPlans, CustomWorkout

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Users, Memberships, MembershipPlans, CustomWorkout, UserGoal, DailyMeals

from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Users, Memberships, MembershipPlans, CustomWorkout, 
    DailyMeals, UserGoal, WeightLog, StrengthRecords, Attendance
)

from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Users, Memberships, MembershipPlans, CustomWorkout, 
    DailyMeals, UserGoal, WeightLog, StrengthRecords, Attendance,
    Trainers, TrainerBookings  # 🔥 Add these imports
)

def dashboard_view(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('/login/')
    
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return redirect('/login/')
    
    today = timezone.now().date()
    
    # ========== MEMBERSHIP DATA ==========
    current_membership = Memberships.objects.filter(user_id=user_id, status='active').first()
    
    if current_membership:
        current_plan = current_membership.plan
        plan_name = current_plan.plan_name
        plan_price = current_plan.price
        end_date = current_membership.end_date
    else:
        plan_name = "No Active Plan"
        plan_price = 0
        end_date = None
    
    # ========== WORKOUT DATA ==========
    current_day = "Monday"
    today_workouts = CustomWorkout.objects.filter(
        user_id=user_id, 
        day_name=current_day
    ).count()
    
    total_workouts = CustomWorkout.objects.filter(user_id=user_id).count()
    
    # ========== WEEKLY WORKOUTS (Last 7 days) ==========
    week_ago = today - timedelta(days=7)
    weekly_workouts = CustomWorkout.objects.filter(
        user_id=user_id,
        created_at__date__gte=week_ago
    ).count()
    
    # ========== ATTENDANCE STREAK ==========
    attendance_dates = Attendance.objects.filter(user_id=user_id).values_list('attendance_date', flat=True).order_by('attendance_date')
    attendance_set = set(attendance_dates)
    
    current_streak = 0
    check_date = today
    while check_date in attendance_set:
        current_streak += 1
        check_date -= timedelta(days=1)
    
    # ========== STRENGTH GOAL (Best Record) ==========
    best_strength = StrengthRecords.objects.filter(user_id=user_id).order_by('-weight_kg').first()
    
    if best_strength:
        best_exercise = best_strength.exercise_name
        best_weight = float(best_strength.weight_kg)
        best_reps = best_strength.reps
    else:
        best_exercise = "No record"
        best_weight = 0
        best_reps = 0
    
    # ========== WEIGHT CHANGE DATA ==========
    weight_logs = WeightLog.objects.filter(user_id=user_id).order_by('date_recorded')
    
    if weight_logs.count() >= 2:
        first_weight = weight_logs.first().weight_kg
        last_weight = weight_logs.last().weight_kg
        weight_change = float(last_weight) - float(first_weight)
        weight_change_kg = round(weight_change, 1)
        weight_change_percent = round((weight_change / float(first_weight)) * 100, 1)
        if weight_change < 0:
            weight_change_direction = 'loss'
        else:
            weight_change_direction = 'gain'
    else:
        weight_change_kg = 0
        weight_change_percent = 0
        weight_change_direction = None
    
    # ========== MEAL TRACKER DATA ==========
    today_meals = DailyMeals.objects.filter(user_id=user_id, meal_date=today)
    today_calories = sum(meal.calories for meal in today_meals)
    today_protein = sum(meal.protein for meal in today_meals)
    
    user_goal = UserGoal.objects.filter(user_id=user_id).first()
    if user_goal:
        goal_calories = user_goal.daily_calories
        goal_protein = user_goal.daily_protein
        remaining_calories = goal_calories - today_calories
        remaining_protein = goal_protein - today_protein
    else:
        goal_calories = 0
        goal_protein = 0
        remaining_calories = 0
        remaining_protein = 0
    
    if goal_calories > 0:
        calorie_percentage = int((today_calories / goal_calories) * 100)
    else:
        calorie_percentage = 0
    
    # ========== 🔥 NEW: TRAINER BOOKING DATA ==========
    # Count of active trainers
    total_trainers = Trainers.objects.filter(is_active=True).count()
    
    # Get user's next upcoming booking
    next_booking = TrainerBookings.objects.filter(
        user_id=user_id,
        booking_status='confirmed',
        booking_date__gte=today
    ).order_by('booking_date', 'booking_time').first()
    
    if next_booking:
        next_booking_display = f"{next_booking.booking_date.strftime('%d %b')} at {next_booking.booking_time.strftime('%I:%M %p')}"
        next_trainer_name = next_booking.trainer.name
    else:
        next_booking_display = "No upcoming sessions"
        next_trainer_name = None
    
    context = {
        'user_name': user.name,
        # Membership
        'plan_name': plan_name,
        'plan_price': plan_price,
        'end_date': end_date,
        # Workout
        'today_workouts': today_workouts,
        'total_workouts': total_workouts,
        'weekly_workouts': weekly_workouts,
        # Attendance Streak
        'current_streak': current_streak,
        # Strength Goal
        'best_exercise': best_exercise,
        'best_weight': best_weight,
        'best_reps': best_reps,
        # Weight Change
        'weight_change_kg': weight_change_kg,
        'weight_change_percent': weight_change_percent,
        'weight_change_direction': weight_change_direction,
        # Meal Tracker
        'today_calories': today_calories,
        'today_protein': today_protein,
        'goal_calories': goal_calories,
        'goal_protein': goal_protein,
        'remaining_calories': remaining_calories if remaining_calories > 0 else 0,
        'remaining_protein': remaining_protein if remaining_protein > 0 else 0,
        'calorie_percentage': calorie_percentage,
        'has_goal': user_goal is not None,
        # 🔥 NEW: Trainer Booking Data
        'total_trainers': total_trainers,
        'next_booking_display': next_booking_display,
        'next_trainer_name': next_trainer_name,
        'has_next_booking': next_booking is not None,
    }
    
    return render(request, 'user/dashboard.html', context)

# def membership_view(req):
#     return render(req,'user/membership.html')

from .models import Users, Memberships, MembershipPlans, Payments

from django.shortcuts import render, redirect
from .models import Users, Memberships, MembershipPlans, Payments

def membership_view(request):
    # 🔥 Session se user_id lo (hardcoded ki jagah)
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('/login/')
    
    # 🔥 Check karo user exist karta hai ya nahi
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return redirect('/login/')
    
    # Fetch current membership
    current_membership = Memberships.objects.filter(user_id=user_id, status='active').first()
    
    if current_membership:
        current_plan = current_membership.plan
        # Convert features string to list
        if current_plan.features:
            current_plan.features_list = [f.strip() for f in current_plan.features.split(',')]
        else:
            current_plan.features_list = []
    else:
        current_plan = None
    
    # Fetch all active plans
    all_plans = MembershipPlans.objects.filter(is_active=True)
    
    # Add features_list to each plan
    for plan in all_plans:
        if plan.features:
            plan.features_list = [f.strip() for f in plan.features.split(',')]
        else:
            plan.features_list = ['Gym Access']
    
    # Fetch payment history for current membership
    if current_membership:
        payments = Payments.objects.filter(membership=current_membership).order_by('-payment_date')
    else:
        payments = []
    
    context = {
        'current_membership': current_membership,
        'current_plan': current_plan,
        'all_plans': all_plans,
        'payments': payments,
        'user_name': user.name,  # 🔥 User name bhi bhej do
    }
    
    return render(request, 'user/membership.html', context)



def payment_view(request):
    """Payment page view"""
    amount = request.GET.get('amount', '6000')
    plan = request.GET.get('plan', 'premium')
    current_plan = request.GET.get('current_plan', 'Gold')
    
    # Plan prices
    plan_prices = {
        'basic': 5000,
        'gold': 12000,
        'premium': 18000
    }
    
    target_price = plan_prices.get(plan, 18000)
    current_price = plan_prices.get(current_plan.lower(), 12000)
    
    context = {
        'amount': amount,
        'target_plan': plan.capitalize(),
        'target_price': target_price,
        'current_plan': current_plan,
        'current_price': current_price,
    }
    
    return render(request, 'user/payment.html', context)




# ==================== WORKOUT PLANS VIEWS ====================
# Ye code apne existing views.py ke end mein add karo
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users, CustomWorkout

# ==================== WORKOUT PLANS VIEWS ====================

def workout_custom(request):
    """Workout plan page - client can see their workouts"""
    # 🔥 Session se user_id lo
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('/login/')
    
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return redirect('/login/')
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    selected_day = request.GET.get('day', 'Monday')
    
    workouts = CustomWorkout.objects.filter(
        user=user,
        day_name=selected_day
    ).order_by('muscle_group')
    
    return render(request, 'user/workout_custom.html', {
        'days': days,
        'selected_day': selected_day,
        'workouts': workouts,
        'user_name': user.name,
    })


@csrf_exempt
def add_workout(request):
    """Add new exercise to workout plan"""
    if request.method == 'POST':
        try:
            # 🔥 Session se user_id lo
            user_id = request.session.get('user_id')
            
            if not user_id:
                return JsonResponse({'success': False, 'message': 'User not logged in'})
            
            user = Users.objects.get(user_id=user_id)
            
            data = json.loads(request.body)
            workout = CustomWorkout.objects.create(
                user=user,
                day_name=data.get('day_name'),
                muscle_group=data.get('muscle_group'),
                exercise_name=data.get('exercise_name'),
                sets=data.get('sets', 3),
                reps=data.get('reps', '12'),
                notes=data.get('notes', '')
            )
            return JsonResponse({'success': True, 'id': workout.id, 'message': 'Exercise added!'})
        except Users.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def get_workout(request, id):
    """Get single workout exercise for editing"""
    # 🔥 Session se user_id lo
    user_id = request.session.get('user_id')
    
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    
    try:
        user = Users.objects.get(user_id=user_id)
        workout = CustomWorkout.objects.get(id=id, user=user)
        return JsonResponse({
            'id': workout.id,
            'day_name': workout.day_name,
            'muscle_group': workout.muscle_group,
            'exercise_name': workout.exercise_name,
            'sets': workout.sets,
            'reps': workout.reps,
            'notes': workout.notes or '',
        })
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found'})
    except CustomWorkout.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Workout not found'})


@csrf_exempt
def update_workout(request, id):
    """Update existing exercise"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            
            if not user_id:
                return JsonResponse({'success': False, 'message': 'Not logged in'})
            
            user = Users.objects.get(user_id=user_id)
            workout = CustomWorkout.objects.get(id=id, user=user)
            data = json.loads(request.body)
            
            workout.day_name = data.get('day_name')
            workout.muscle_group = data.get('muscle_group')
            workout.exercise_name = data.get('exercise_name')
            workout.sets = data.get('sets')
            workout.reps = data.get('reps')
            workout.notes = data.get('notes', '')
            workout.save()
            
            return JsonResponse({'success': True, 'message': 'Exercise updated!'})
        except Users.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})
        except CustomWorkout.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Workout not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@csrf_exempt
def delete_workout(request, id):
    """Delete exercise from workout plan"""
    if request.method == 'DELETE':
        try:
            user_id = request.session.get('user_id')
            
            if not user_id:
                return JsonResponse({'success': False, 'message': 'Not logged in'})
            
            user = Users.objects.get(user_id=user_id)
            workout = CustomWorkout.objects.get(id=id, user=user)
            workout.delete()
            
            return JsonResponse({'success': True, 'message': 'Exercise deleted!'})
        except Users.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})
        except CustomWorkout.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Workout not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def diet_plans_view(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('/login/')
    
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return redirect('/login/')
    
    return render(request, 'user/diet_plans.html', {'user_name': user.name})






import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Users, UserGoal, DailyMeals, MealHistory
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import UserGoal

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Users, UserGoal, DailyMeals

def diet_plans_view(request):
    # 🔥 Sirf GET request handle karega
    if request.method != 'GET':
        return redirect('/user/dash/diet/')
    
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('/user/login/')
    
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return redirect('/user/login/')
    
    # Check if user has already set a goal
    user_goal = UserGoal.objects.filter(user_id=user_id).first()
    
    today = timezone.now().date()
    
    # Get today's meals
    breakfast_items = DailyMeals.objects.filter(user_id=user_id, meal_date=today, meal_type='breakfast')
    lunch_items = DailyMeals.objects.filter(user_id=user_id, meal_date=today, meal_type='lunch')
    snacks_items = DailyMeals.objects.filter(user_id=user_id, meal_date=today, meal_type='snacks')
    dinner_items = DailyMeals.objects.filter(user_id=user_id, meal_date=today, meal_type='dinner')
    
    # Calculate totals
    total_calories = sum(item.calories for item in list(breakfast_items) + list(lunch_items) + list(snacks_items) + list(dinner_items))
    total_protein = sum(item.protein for item in list(breakfast_items) + list(lunch_items) + list(snacks_items) + list(dinner_items))
    
    context = {
        'user_name': user.name,
        'has_goal': user_goal is not None,
        'breakfast_items': breakfast_items,
        'lunch_items': lunch_items,
        'snacks_items': snacks_items,
        'dinner_items': dinner_items,
        'total_calories': total_calories,
        'total_protein': total_protein,
    }
    
    if user_goal:
        context['daily_calories_target'] = user_goal.daily_calories
        context['daily_protein_target'] = user_goal.daily_protein
        context['remaining_calories'] = user_goal.daily_calories - total_calories
        context['remaining_protein'] = user_goal.daily_protein - total_protein
        context['goal_type'] = user_goal.goal_type
    else:
        context['daily_calories_target'] = 0
        context['daily_protein_target'] = 0
    
    return render(request, 'user/diet_plans.html', context)

def api_save_goal(request):
    print("=" * 50)
    print("API SAVE GOAL CALLED")
    
    # Get user_id from session
    user_id = request.session.get('user_id')
    print(f"User ID from session: {user_id}")
    
    if not user_id:
        return JsonResponse({'success': False, 'message': 'User not logged in'})
    
    try:
        # Parse JSON data
        data = json.loads(request.body)
        print(f"Received data: {data}")
        
        # Get or create user goal
        goal, created = UserGoal.objects.update_or_create(
            user_id=user_id,
            defaults={
                'goal_type': data.get('goal_type'),
                'daily_calories': data.get('daily_calories'),
                'daily_protein': data.get('daily_protein'),
                'age': data.get('age'),
                'weight': data.get('weight'),
                'height': data.get('height'),
                'gender': data.get('gender'),
                'activity_level': data.get('activity_level'),
            }
        )
        
        print(f"Goal {'created' if created else 'updated'} successfully")
        return JsonResponse({'success': True, 'message': 'Goal saved successfully!'})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)})


def api_today_meals(request):
    user_id = request.session.get('user_id')
    if not user_id: return JsonResponse({'success': False, 'message': 'Not logged in'})
    goal = UserGoal.objects.filter(user_id=user_id).first()
    if not goal: return JsonResponse({'success': False, 'has_goal': False})
    today = timezone.now().date()
    meals = DailyMeals.objects.filter(user_id=user_id, meal_date=today)
    meals_data = {'breakfast': [], 'lunch': [], 'snacks': [], 'dinner': []}
    for m in meals: meals_data[m.meal_type].append({'name': m.food_name, 'quantity': m.quantity, 'calories': m.calories, 'protein': m.protein})
    return JsonResponse({'success': True, 'meals': meals_data, 'target_calories': goal.daily_calories, 'target_protein': goal.daily_protein})

@csrf_exempt
def api_add_meal(request):
    if request.method != 'POST': return JsonResponse({'success': False})
    user_id = request.session.get('user_id')
    if not user_id: return JsonResponse({'success': False})
    data = json.loads(request.body)
    DailyMeals.objects.create(user_id=user_id, meal_date=timezone.now().date(), meal_type=data['meal_type'], food_name=data['food_name'], quantity=data.get('quantity', ''), calories=data['calories'], protein=data.get('protein', 0))
    return api_today_meals(request)

@csrf_exempt
def api_delete_meal(request):
    if request.method != 'POST': return JsonResponse({'success': False})
    user_id = request.session.get('user_id')
    if not user_id: return JsonResponse({'success': False})
    data = json.loads(request.body)
    DailyMeals.objects.filter(user_id=user_id, meal_date=timezone.now().date(), meal_type=data['meal_type'], food_name=data['food_name'], calories=data['calories']).delete()
    return api_today_meals(request)

@csrf_exempt
def api_end_day(request):
    if request.method != 'POST': return JsonResponse({'success': False})
    user_id = request.session.get('user_id')
    if not user_id: return JsonResponse({'success': False})
    goal = UserGoal.objects.filter(user_id=user_id).first()
    if not goal: return JsonResponse({'success': False, 'message': 'No goal set'})
    today = timezone.now().date()
    meals = DailyMeals.objects.filter(user_id=user_id, meal_date=today)
    total_cal = sum(m.calories for m in meals)
    total_pro = sum(m.protein for m in meals)
    MealHistory.objects.create(user_id=user_id, record_date=today, total_calories=total_cal, total_protein=total_pro, target_calories=goal.daily_calories, target_protein=goal.daily_protein, goal_type=goal.goal_type)
    meals.delete()
    return JsonResponse({'success': True, 'message': f'Saved! Total: {total_cal} cal, {total_pro}g protein'})








from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, Avg
from .models import Users, UserGoal, WeightLog, StrengthRecords, BodyMeasurements, WorkoutCompletionLog, UserBadges, DailyMeals

def progress_tracking_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/user/login/')
    
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return redirect('/user/login/')
    
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    # Weekly activity
    weekly_activity = []
    for i in range(7):
        day = today - timedelta(days=i)
        day_name = day.strftime('%a')
        count = WorkoutCompletionLog.objects.filter(user_id=user_id, workout_date=day).count()
        weekly_activity.append({'day': day_name, 'count': count})
    weekly_activity.reverse()
    
    context = {
        'user_name': user.name,
        'total_workouts': WorkoutCompletionLog.objects.filter(user_id=user_id, workout_date__gte=week_ago).count(),
        'total_calories': WorkoutCompletionLog.objects.filter(user_id=user_id, workout_date__gte=week_ago).aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
        'total_minutes': WorkoutCompletionLog.objects.filter(user_id=user_id, workout_date__gte=week_ago).aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0,
        'active_days': WorkoutCompletionLog.objects.filter(user_id=user_id, workout_date__gte=week_ago).values('workout_date').distinct().count(),
        'weekly_activity': weekly_activity,
        'avg_calories': 0,
        'avg_protein': 0,
    }
    
    return render(request, 'user/progress_tracking.html', context)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
from .models import Users, WeightLog, StrengthRecords, WorkoutCompletionLog

# ========== PROGRESS TRACKING PAGE VIEW ==========
def progress_tracking_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/user/login/')
    return render(request, 'user/progress_tracking.html')


# ========== ADD APIs ==========
@csrf_exempt
@require_http_methods(["POST"])
def api_add_weight(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    try:
        data = json.loads(request.body)
        WeightLog.objects.create(
            user_id=user_id,
            weight_kg=data['weight_kg'],
            date_recorded=data['date_recorded']
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_add_strength(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    try:
        data = json.loads(request.body)
        StrengthRecords.objects.create(
            user_id=user_id,
            exercise_name=data['exercise_name'],
            weight_kg=data['weight_kg'],
            reps=data['reps'],
            date_recorded=data['date_recorded']
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_add_workout_log(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    try:
        data = json.loads(request.body)
        WorkoutCompletionLog.objects.create(
            user_id=user_id,
            workout_date=data['workout_date'],
            workout_name=data.get('workout_name', ''),
            calories_burned=data.get('calories_burned', 0),
            duration_minutes=data.get('duration_minutes', 0)
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# ========== GET APIs ==========
def api_get_workout_stats(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    logs = WorkoutCompletionLog.objects.filter(user_id=user_id)
    return JsonResponse({
        'success': True,
        'total_workouts': logs.count(),
        'total_calories': sum(l.calories_burned for l in logs),
        'total_minutes': sum(l.duration_minutes for l in logs),
        'active_days': logs.values('workout_date').distinct().count()
    })


def api_get_weight_data(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    weights = WeightLog.objects.filter(user_id=user_id).order_by('date_recorded')
    weight_data = [
        {'date': w.date_recorded.strftime('%d %b'), 'weight': float(w.weight_kg)}
        for w in weights
    ]
    return JsonResponse({'success': True, 'weight_data': weight_data})

def api_get_strength_data(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    
    exercises = ['Bench Press', 'Squat', 'Deadlift', 'Shoulder Press']
    strength_data = []
    
    for ex in exercises:
        records = StrengthRecords.objects.filter(
            user_id=user_id, 
            exercise_name=ex
        ).order_by('date_recorded')
        
        if records.exists():
            first = records.first()
            last = records.last()
            
            # Calculate volume (weight × reps)
            first_volume = first.weight_kg * first.reps
            last_volume = last.weight_kg * last.reps
            
            # Progress percentage
            if first_volume > 0:
                progress = round(((last_volume - first_volume) / first_volume) * 100, 1)
            else:
                progress = 0
            
            strength_data.append({
                'name': ex,
                'starting_weight': float(first.weight_kg),
                'starting_reps': first.reps,
                'starting_volume': round(first_volume, 1),
                'current_weight': float(last.weight_kg),
                'current_reps': last.reps,
                'current_volume': round(last_volume, 1),
                'progress': progress
            })
    
    return JsonResponse({'success': True, 'strength_data': strength_data})


def api_get_weekly_activity(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    today = datetime.now().date()
    week = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        exists = WorkoutCompletionLog.objects.filter(user_id=user_id, workout_date=day).exists()
        week.append({'day': day.strftime('%a'), 'active': exists})
    return JsonResponse({'success': True, 'week': week})


def api_get_badges(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    badges = []
    logs = WorkoutCompletionLog.objects.filter(user_id=user_id)
    total = logs.count()
    if total >= 5: badges.append({'badge_name': '5 Workouts', 'badge_icon': '🌟'})
    if total >= 25: badges.append({'badge_name': '25 Workouts', 'badge_icon': '⭐'})
    if total >= 50: badges.append({'badge_name': '50 Workouts', 'badge_icon': '🏆'})
    if total >= 100: badges.append({'badge_name': '100 Workouts', 'badge_icon': '💪'})
    today = datetime.now().date()
    streak = 0
    for i in range(30):
        day = today - timedelta(days=i)
        if WorkoutCompletionLog.objects.filter(user_id=user_id, workout_date=day).exists():
            streak += 1
        else:
            break
    if streak >= 7: badges.append({'badge_name': f'{streak} Day Streak', 'badge_icon': '🔥'})
    return JsonResponse({'success': True, 'badges': badges})

@csrf_exempt
@require_http_methods(["POST"])
def api_reset_progress(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    
    try:
        # Delete all workout logs
        WorkoutCompletionLog.objects.filter(user_id=user_id).delete()
        
        return JsonResponse({'success': True, 'message': 'Progress reset successfully!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    










    from datetime import datetime, timedelta
from django.db.models import Count, Q
from .models import Attendance, Users

def attendance_view(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('/user/login/')
    
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return redirect('/user/login/')
    
    today = datetime.now().date()
    
    # ========== TODAY'S CHECK-IN STATUS ==========
    today_attendance = Attendance.objects.filter(user_id=user_id, attendance_date=today).first()
    has_checked_in_today = today_attendance is not None
    
    # ========== STREAK CALCULATION ==========
    # Get all attendance dates
    attendance_dates = Attendance.objects.filter(user_id=user_id).values_list('attendance_date', flat=True).order_by('attendance_date')
    attendance_set = set(attendance_dates)
    
    # Calculate current streak
    current_streak = 0
    check_date = today
    while check_date in attendance_set:
        current_streak += 1
        check_date -= timedelta(days=1)
    
    # Calculate best streak
    best_streak = 0
    temp_streak = 0
    prev_date = None
    
    for att_date in sorted(attendance_dates):
        if prev_date and (att_date - prev_date).days == 1:
            temp_streak += 1
        else:
            temp_streak = 1
        best_streak = max(best_streak, temp_streak)
        prev_date = att_date
    
    # ========== TOTAL STATS ==========
    total_checkins = attendance_dates.count()
    
    # This month stats
    first_day_of_month = today.replace(day=1)
    this_month_checkins = Attendance.objects.filter(
        user_id=user_id, 
        attendance_date__gte=first_day_of_month
    ).count()
    days_in_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    days_in_month = days_in_month.day
    month_percentage = int((this_month_checkins / days_in_month) * 100) if days_in_month > 0 else 0
    
    # ========== WEEKLY ACTIVITY (Last 7 days) ==========
    weekly_activity = []
    week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    today_weekday = today.weekday()
    start_of_week = today - timedelta(days=today_weekday)
    
    for i in range(7):
        day_date = start_of_week + timedelta(days=i)
        attended = day_date in attendance_set
        weekly_activity.append({
            'day': week_days[i],
            'date': day_date.strftime('%d %b'),
            'active': attended,
            'is_today': day_date == today
        })
    
    # ========== MONTHLY CALENDAR ==========
    # Get current month and year
    current_month = today.month
    current_year = today.year
    
    # Get first day of month and number of days
    first_day = today.replace(day=1)
    last_day = (first_day.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    days_in_month = last_day.day
    
    # Get weekday of first day (0 = Monday, 6 = Sunday)
    first_weekday = first_day.weekday()
    
    # Build calendar grid
    calendar_grid = []
    week = []
    
    # Add empty cells for days before month starts
    for i in range(first_weekday):
        week.append({'day': None, 'date': None, 'attended': False})
    
    # Add days of the month
    for day_num in range(1, days_in_month + 1):
        date_obj = today.replace(day=day_num)
        attended = date_obj in attendance_set
        week.append({
            'day': day_num,
            'date': date_obj,
            'attended': attended,
            'is_today': date_obj == today
        })
        
        if len(week) == 7:
            calendar_grid.append(week)
            week = []
    
    # Add remaining empty cells
    if week:
        while len(week) < 7:
            week.append({'day': None, 'date': None, 'attended': False})
        calendar_grid.append(week)
    
    # ========== RECENT ACTIVITY LOG ==========
    recent_activities = Attendance.objects.filter(user_id=user_id).order_by('-attendance_date')[:10]
    
    # ========== STREAK BADGES ==========
    badges = []
    if current_streak >= 7:
        badges.append({'name': '7-Day Warrior', 'icon': '🔥', 'streak': 7})
    if current_streak >= 14:
        badges.append({'name': 'Consistent', 'icon': '⚡', 'streak': 14})
    if current_streak >= 30:
        badges.append({'name': 'Dedicated', 'icon': '💪', 'streak': 30})
    if best_streak >= 60:
        badges.append({'name': 'Iron Will', 'icon': '🏆', 'streak': 60})
    if best_streak >= 90:
        badges.append({'name': 'Legend', 'icon': '👑', 'streak': 90})
    if total_checkins >= 100:
        badges.append({'name': 'Centurion', 'icon': '🌟', 'count': 100})
    
    # ========== MOST ACTIVE DAY ==========
    day_counts = {
        'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0
    }
    for att in Attendance.objects.filter(user_id=user_id):
        day_name = att.attendance_date.strftime('%A')
        day_counts[day_name] += 1
    most_active_day = max(day_counts, key=day_counts.get) if total_checkins > 0 else None
    most_active_day_count = day_counts.get(most_active_day, 0)
    
    context = {
        'user_name': user.name,
        # Status
        'has_checked_in_today': has_checked_in_today,
        'today_attendance': today_attendance,
        # Streaks
        'current_streak': current_streak,
        'best_streak': best_streak,
        # Stats
        'total_checkins': total_checkins,
        'this_month_checkins': this_month_checkins,
        'days_in_month': days_in_month,
        'month_percentage': month_percentage,
        # Data for display
        'weekly_activity': weekly_activity,
        'calendar_grid': calendar_grid,
        'current_month_name': first_day.strftime('%B'),
        'current_year': current_year,
        'recent_activities': recent_activities,
        'badges': badges,
        'most_active_day': most_active_day,
        'most_active_day_count': most_active_day_count,
    }
    
    return render(request, 'user/attendance.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def api_mark_attendance(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    
    today = datetime.now().date()
    
    # Check if already marked
    if Attendance.objects.filter(user_id=user_id, attendance_date=today).exists():
        return JsonResponse({'success': False, 'message': 'Already checked in today!'})
    
    try:
        data = json.loads(request.body)
        workout_name = data.get('workout_name', '')
        notes = data.get('notes', '')
        
        Attendance.objects.create(
            user_id=user_id,
            attendance_date=today,
            check_in_time=datetime.now().time(),
            workout_name=workout_name,
            notes=notes
        )
        
        return JsonResponse({'success': True, 'message': 'Attendance marked successfully!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    










from datetime import datetime, timedelta
from .models import Trainers, TrainerBookings, TrainerReviews, BookingPackages

def trainer_booking_view(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('/user/login/')
    
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return redirect('/user/login/')
    
    today = datetime.now().date()
    
    # Get all active trainers
    trainers = Trainers.objects.filter(is_active=True)
    
    # Get user's upcoming bookings
    upcoming_bookings = TrainerBookings.objects.filter(
        user_id=user_id,
        booking_date__gte=today,
        booking_status__in=['confirmed', 'pending']
    ).order_by('booking_date', 'booking_time')
    
    # Get user's past bookings
    past_bookings = TrainerBookings.objects.filter(
        user_id=user_id,
        booking_date__lt=today
    ).order_by('-booking_date')[:10]
    
    # Get packages
    packages = BookingPackages.objects.filter(is_active=True)
    
    # Stats
    total_bookings = TrainerBookings.objects.filter(user_id=user_id).count()
    completed_bookings = TrainerBookings.objects.filter(user_id=user_id, booking_status='completed').count()
    
    # Get reviews for past bookings
    for booking in past_bookings:
        try:
            booking.review = TrainerReviews.objects.get(booking_id=booking.id)
        except TrainerReviews.DoesNotExist:
            booking.review = None
    
    context = {
        'user_name': user.name,
        'trainers': trainers,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'packages': packages,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
    }
    
    return render(request, 'user/trainer_booking.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def api_get_trainer_slots(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    
    data = json.loads(request.body)
    trainer_id = data.get('trainer_id')
    booking_date = data.get('booking_date')
    
    # Get existing bookings for that trainer on that date
    existing_bookings = TrainerBookings.objects.filter(
        trainer_id=trainer_id,
        booking_date=booking_date,
        booking_status__in=['confirmed', 'pending']
    ).values_list('booking_time', flat=True)
    
    existing_times = set(existing_bookings)
    
    # Available time slots (9 AM to 6 PM, 1 hour slots)
    all_slots = []
    for hour in range(9, 19):
        time_str = f"{hour:02d}:00:00"
        if time_str not in existing_times:
            all_slots.append(f"{hour:02d}:00")
    
    return JsonResponse({'success': True, 'slots': all_slots})


@csrf_exempt
@require_http_methods(["POST"])
def api_create_booking(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    
    try:
        data = json.loads(request.body)
        
        trainer = Trainers.objects.get(id=data['trainer_id'])
        
        booking = TrainerBookings.objects.create(
            user_id=user_id,
            trainer_id=data['trainer_id'],
            booking_date=data['booking_date'],
            booking_time=data['booking_time'],
            duration_minutes=data.get('duration', 60),
            goal=data.get('goal', ''),
            total_amount=trainer.price_per_session,
            payment_status='pending',
            booking_status='confirmed'
        )
        
        return JsonResponse({'success': True, 'booking_id': booking.id, 'message': 'Booking confirmed!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_cancel_booking(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    
    try:
        data = json.loads(request.body)
        booking = TrainerBookings.objects.get(id=data['booking_id'], user_id=user_id)
        booking.booking_status = 'cancelled'
        booking.save()
        return JsonResponse({'success': True, 'message': 'Booking cancelled!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def api_submit_review(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})
    
    try:
        data = json.loads(request.body)
        booking = TrainerBookings.objects.get(id=data['booking_id'], user_id=user_id)
        
        TrainerReviews.objects.create(
            booking_id=booking.id,
            rating=data['rating'],
            feedback=data.get('feedback', '')
        )
        
        # Update trainer rating
        trainer = booking.trainer
        avg_rating = TrainerReviews.objects.filter(booking__trainer_id=trainer.id).aggregate(models.Avg('rating'))['rating__avg']
        trainer.rating = round(avg_rating, 1)
        trainer.save()
        
        return JsonResponse({'success': True, 'message': 'Review submitted!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})