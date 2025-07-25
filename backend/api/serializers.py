from rest_framework import serializers
from .models import Cities, Activities, Elders, Volunteers, Appointments, CustomUser, CustomUserManager


class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ['id', 'title', 'zipcode', 'lat', 'lng']


class ActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = ['id', 'name']

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id','email','first_name','last_name','role', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ElderSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    city = CitiesSerializer()
    age = serializers.ReadOnlyField()

    class Meta:
        model = Elders
        fields = ['id', 'user', 'job', 'date_of_birth', 'city', 'description','image_url', 'phone_number', 'age']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        city_data = validated_data.pop('city')
    

        password = user_data.pop('password', None)
        
        user = CustomUser.objects.create_user(password=password, **user_data)
        city, _ = Cities.objects.get_or_create(**city_data)
        elder = Elders.objects.create(user=user,city=city, **validated_data)
        return elder
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        city_data = validated_data.pop('city', None)

        if user_data:
            user = instance.user
            password = user_data.pop('password', None)

            for attr, value in user_data.items():
                setattr(user, attr, value)

            if password:
                user.set_password(password)

            user.save()

        if city_data:
            city, _ = Cities.objects.get_or_create(**city_data)
            instance.city = city

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class VolunteerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    city = CitiesSerializer()

    class Meta:
        model = Volunteers
        fields = ['id', 'user', 'city', 'phone_number', 'url_image']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        city_data = validated_data.pop('city')
        password = user_data.pop('password', None)

        user = CustomUser.objects.create_user(password=password, **user_data)
        city, _ = Cities.objects.get_or_create(**city_data)
        volunteer = Volunteers.objects.create(user=user, city=city, **validated_data)
        return volunteer
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        city_data = validated_data.pop('city', None)

        if user_data:
            user = instance.user
            password = user_data.pop('password', None)

            for attr, value in user_data.items():
                setattr(user, attr, value)

            if password:
                user.set_password(password)

            user.save()

        if city_data:
            city, _ = Cities.objects.get_or_create(**city_data)
            instance.city = city

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class AppointmentSerializer(serializers.ModelSerializer):
    activity = serializers.PrimaryKeyRelatedField(queryset=Activities.objects.all())
    elder = serializers.PrimaryKeyRelatedField(queryset=Elders.objects.all())

    volunteer = VolunteerSerializer(read_only=True)

    activity_detail = ActivitiesSerializer(source='activity', read_only=True)
    elder_detail = ElderSerializer(source='elder', read_only=True)
    volunteer_detail = VolunteerSerializer(source='volunteer', read_only=True)

    class Meta:
        model = Appointments
        fields = ['id', 'date', 'activity', 'elder', 'volunteer', 'activity_detail', 'elder_detail', 'volunteer_detail']


    
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")

        try:
            volunteer = request.user.volunteers
        except Volunteers.DoesNotExist:
            raise serializers.ValidationError("Volunteer profile not found for the user")

        appointment = Appointments.objects.create(volunteer=volunteer, **validated_data)
        return appointment
