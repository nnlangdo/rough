from django import forms
from .models import Participant, FamilyMember,Event
from django.db.models import Q
from datetime import datetime, time

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['event','name','age','gender','type_id','number_id','phone','state','district','village','family_members','position','status']
        widgets = {
            'event': forms.Select(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'age': forms.NumberInput(attrs={'class':'form-control','min':18,'max':120}),
            'gender': forms.Select(attrs={'class':'form-control'}),
            'type_id': forms.Select(attrs={'class':'form-control'}),
            'number_id': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.Select(attrs={'class':'form-control'}), 
            'district': forms.Select(attrs={'class':'form-control'}),
            'village': forms.TextInput(attrs={'class':'form-control'}),
            'family_members': forms.NumberInput(attrs={'class':'form-control','max':100}),
            'position': forms.Select(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the current date and time
        current_datetime = datetime.now()

        # Create a datetime object with today's date and time 6:30 AM
        today_630am = datetime.combine(current_datetime.date(), time(6, 30))

        if current_datetime.time() >= time(6, 30):
            # If current time is 6:30 AM or later, exclude events before today
            excluded_events = Event.objects.filter(event_date__lte=current_datetime.date())
        else:
            # If current time is before 6:30 AM, exclude events before or equal to today
            excluded_events = Event.objects.filter(event_date__lt=current_datetime.date())

        # Exclude events with excessive participants
        excluded_event_ids = [
            event.id for event in Event.objects.all() if event.has_excessive_participants()
        ]
        excluded_events = excluded_events.union(Event.objects.filter(id__in=excluded_event_ids))

        # Get the remaining events
        filtered_events = Event.objects.exclude(id__in=excluded_events.values('id'))

        # Set the filtered events as the queryset for the event field
        self.fields['event'].queryset = filtered_events


    def clean(self):
        cleaned_data = super().clean()
        event_date = cleaned_data.get('event').event_date
        participant_position = cleaned_data.get('position')
        participant_status = cleaned_data.get('status')

        if participant_status == 'live':
            main_count = Participant.objects.filter(
                Q(position='main', status='live') | Q(position='waiting', status='live'),
                event__event_date=event_date
            ).count()
            waiting_count = Participant.objects.filter(
                position='waiting', status='live',
                event__event_date=event_date
            ).count()

            if participant_position == 'main' and main_count >= 1:
                raise forms.ValidationError("Only one participant with position 'main' allowed per event date.")
            elif participant_position == 'waiting' and waiting_count >= 2:
                raise forms.ValidationError("Only two participants with position 'waiting' allowed per event date.")    
    
class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['name','gender','age']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'gender': forms.Select(attrs={'class':'form-control'}),
            'age': forms.NumberInput(attrs={'class':'form-control','min':1,'max':120}),
        }