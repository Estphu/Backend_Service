from rest_framework import serializers
from .models import Plan, App, Subscription

class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = ['id', 'name', 'price']    

class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = ['id', 'name', 'description'] 

class SubscriptionSerializer(serializers.ModelSerializer):
    app = serializers.PrimaryKeyRelatedField(queryset=App.objects.all())
    plan = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())

    class Meta:
        model = Subscription
        fields = ['id', 'app', 'plan', 'active']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        print(user)
        if user:
            print(self.fields['plan'].queryset)
            # Filter queryset for app and plan based on the logged-in user
            self.fields['app'].queryset = App.objects.filter(user=user)
            self.fields['plan'].queryset = Plan.objects.filter(user=user)
    
    def to_representation(self, instance):
        user = self.context['request'].user
        # Serialize the instance data
        if instance.user == user:
            # print(instance.user)
            # print(user)
            rep = super(SubscriptionSerializer, self).to_representation(instance)
            rep['app'] = instance.app.name
            rep['plan'] = instance.plan.name
            return rep
        return None