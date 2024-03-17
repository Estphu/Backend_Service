from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # Ensures each user can have unique plan names
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name

class App(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if the app is being created for the first time
        if not self.pk:
            # Creating the App instance
            super(App, self).save(*args, **kwargs)

            # Getting or creating the Free Plan
            free_plan, _ = Plan.objects.get_or_create(user=self.user, name="Free", price=0)

            # Checking if a Subscription already exists for this App
            existing_subscription = Subscription.objects.filter(user=self.user, app=self).first()

            if existing_subscription:
                # Update the existing Subscription
                existing_subscription.plan = free_plan
                existing_subscription.active = True
            # Creating a Subscription for the App with the Free Plan
            else:
                Subscription.objects.create(user=self.user, app=self, plan=free_plan, active=True)

        else:
            super(App, self).save(*args, **kwargs)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    app = models.OneToOneField(App, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.app} - {self.plan}"
    
    def cancel_subscription(self):
        self.active = False
        self.save()