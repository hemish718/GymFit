from django.db import models


    

from django.db import models

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=255, default='')  # 🔥 NEW: Password field
    join_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name

class MembershipPlans(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=50)
    duration_months = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'membership_plans'

class Memberships(models.Model):
    membership_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    plan = models.ForeignKey(MembershipPlans, on_delete=models.CASCADE, db_column='plan_id')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=[
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled')
    ], default='active')
    payment_status = models.CharField(max_length=10, choices=[
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed')
    ], default='pending')

    class Meta:
        db_table = 'memberships'

class Payments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    membership = models.ForeignKey(Memberships, on_delete=models.CASCADE, db_column='membership_id')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=30, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=[
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ], default='success')

    class Meta:
        db_table = 'payments'

from django.db import models

# class WorkoutPlan(models.Model):
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     plan_name = models.CharField(max_length=100)
#     day_of_week = models.CharField(max_length=20)
#     exercise_name = models.CharField(max_length=100)
#     sets = models.IntegerField()
#     reps = models.IntegerField()
#     weight_kg = models.IntegerField(blank=True, null=True)
#     is_completed = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.plan_name} - {self.day_of_week}"


class CustomWorkout(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    day_name = models.CharField(max_length=20)  # Monday, Tuesday...
    muscle_group = models.CharField(max_length=50)
    exercise_name = models.CharField(max_length=100)
    sets = models.IntegerField(default=3)
    reps = models.IntegerField(default=12)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.day_name} - {self.exercise_name}"

    class Meta:
        db_table = 'custom_workout'
class UserGoal(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    goal_type = models.CharField(max_length=50)
    daily_calories = models.IntegerField()
    daily_protein = models.IntegerField()
    age = models.IntegerField()
    weight = models.IntegerField()
    height = models.IntegerField()
    gender = models.CharField(max_length=10)
    activity_level = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_goal'


class DailyMeals(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    meal_date = models.DateField(auto_now_add=True)
    meal_type = models.CharField(max_length=20)
    food_name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50, blank=True, null=True)
    calories = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'daily_meals'


class MealHistory(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    record_date = models.DateField()
    total_calories = models.IntegerField()
    total_protein = models.IntegerField()
    target_calories = models.IntegerField()
    target_protein = models.IntegerField()
    goal_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'meal_history'





class WeightLog(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = models.DateField()
    notes = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'weight_log'


class StrengthRecords(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    exercise_name = models.CharField(max_length=100)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    reps = models.IntegerField()
    date_recorded = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'strength_records'
    
    @property
    def volume(self):
        return float(self.weight_kg) * self.reps

class BodyMeasurements(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    measurement_date = models.DateField()
    chest_inch = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    waist_inch = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    biceps_inch = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    thighs_inch = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'body_measurements'


class WorkoutCompletionLog(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    workout_date = models.DateField()
    workout_name = models.CharField(max_length=100, blank=True, null=True)
    calories_burned = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workout_completion_log'


class UserBadges(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    badge_name = models.CharField(max_length=100)
    badge_icon = models.CharField(max_length=50, blank=True, null=True)
    achieved_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_badges'



class Attendance(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    attendance_date = models.DateField()
    check_in_time = models.TimeField()
    workout_name = models.CharField(max_length=100, blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attendance'
        unique_together = ['user', 'attendance_date']

    def __str__(self):
        return f"{self.user.name} - {self.attendance_date}"
    
    





class Trainers(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    price_per_session = models.IntegerField(default=500)
    bio = models.TextField(blank=True, null=True)
    image_icon = models.CharField(max_length=50, default='👨‍🏫')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'trainers'

    def __str__(self):
        return self.name


class TrainerBookings(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    trainer = models.ForeignKey(Trainers, on_delete=models.CASCADE, db_column='trainer_id')
    booking_date = models.DateField()
    booking_time = models.TimeField()
    duration_minutes = models.IntegerField(default=60)
    session_type = models.CharField(max_length=50, blank=True, null=True)
    goal = models.TextField(blank=True, null=True)
    total_amount = models.IntegerField()
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    booking_status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'trainer_bookings'


class TrainerReviews(models.Model):
    booking = models.ForeignKey(TrainerBookings, on_delete=models.CASCADE, db_column='booking_id')
    rating = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'trainer_reviews'


class BookingPackages(models.Model):
    package_name = models.CharField(max_length=100)
    sessions_count = models.IntegerField()
    price = models.IntegerField()
    validity_days = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'booking_packages'