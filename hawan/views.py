from django.shortcuts import render,redirect,get_object_or_404
from . models import Participant, FamilyMember
from . forms import ParticipantForm, FamilyMemberForm
from .models import Province,District
from django.utils import timezone
from django.forms import inlineformset_factory
# from django.views import View
# Create your views here.

# def view_page(request):
#     context = {
    
#     }
#     return render(request, 'hawan/view_page.html')

# def view_page(request):
#     if request.method == 'POST':
#         form = ParticipantForm(request.POST)
#         if form.is_valid():
#             participant = form.save(commit=False)
#             participant.registered_by = request.user
#             participant.save()
#             return redirect('hawan:view_page')
#     else:
#         form = ParticipantForm()
#     context = {
#         'form':'form',
#     }
#     return render(request, 'hawan/view_page.html',context)

def district(request):
    province = request.GET.get('state')
    districts = District.objects.filter(province=province)
    context = {
        'districts':districts,
    }
    return render(request, 'partials/districts.html',context)

# def add_family_member_field(request):
#     if request.method == "POST":
#         pass

#     return render(request, 'partials/add_familymember_form.html')

# def view_page(request):
#     if request.method == 'POST':
#         form = ParticipantForm(request.POST)
#         family_member_forms = [FamilyMemberForm(request.POST, prefix=f'family_member_{i}') for i in range(5)]

#         if form.is_valid() and all([fm_form.is_valid() for fm_form in family_member_forms]):
#             participant = form.save()
#             for fm_form in family_member_forms:
#                 if fm_form.cleaned_data.get('name'):
#                     FamilyMember.objects.create(participant=participant, **fm_form.cleaned_data)
#             return redirect('hawan:view_page')  # Redirect to the desired URL upon successful submission
#     else:
#         form = ParticipantForm()
#         family_member_forms = [FamilyMemberForm(prefix=f'family_member_{i}') for i in range(5)]  # You can adjust the number of forms as needed

#     provinces = Province.objects.all()  # Assuming you have this queryset
#     context = {
#         'form': form,
#         'family_member_forms': family_member_forms,
#         'provinces': provinces,
#     }
#     return render(request, 'hawan/view_page.html', context)


def index(request):
    return render(request,'hawan/index.html')

def view_page(request):
    provinces = Province.objects.all()
    current_date = timezone.now().date()  # Get today's date
    participants = Participant.objects.filter(event__event_date__gte=current_date)
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.registered_by = request.user
            participant.save()
            num_family_members = participant.family_members

            if num_family_members >= 1:
                return redirect('hawan:add_family_members', participant_id=participant.id, num_family_members=num_family_members)
            else:
                return redirect('hawan:view_page')  # Redirect to the desired view page
    else:
        form = ParticipantForm()
    context = {
        'form':form,
        'provinces':provinces,
        'participants':participants,
    }
    return render(request, 'hawan/view_page.html', context)

# def add_family_members(request, participant_id):
#     participant = get_object_or_404(Participant, id=participant_id)

#     if request.method == 'POST':
#         fm_form = FamilyMemberForm(request.POST or None)
#         if fm_form.is_valid():
#             family_member = fm_form.save(commit=False)
#             family_member.participant = participant
#             family_member.save()
#             return redirect('hawan:view_page')
#     else:
#         fm_form = FamilyMemberForm()

#     return render(request, 'partials/add_family_members.html', {
#         'participant': participant,
#         'fm_form': fm_form,
#     })

def add_family_members(request, participant_id, num_family_members):
    participant = get_object_or_404(Participant, id=participant_id)

    if request.method == 'POST':
        fm_forms = [FamilyMemberForm(request.POST, prefix=f'family_member_{i}') for i in range(num_family_members)]

        if all([fm_form.is_valid() for fm_form in fm_forms]):
            # Save the family member instances
            for fm_form in fm_forms:
                family_member = fm_form.save(commit=False)
                family_member.participant = participant
                family_member.save()

            # Redirect to the desired URL upon successful submission
            return redirect('hawan:view_page')
    else:
        fm_forms = [FamilyMemberForm(prefix=f'family_member_{i}') for i in range(num_family_members)]

    context = {
        'participant': participant,
        'fm_forms': fm_forms,
        'num_family_members': num_family_members,
    }
    return render(request, 'partials/add_family_members.html', context)

# def add_family_form(request,participant_id):
#     participant = get_object_or_404(Participant, id=participant_id)
#     if request.method == 'POST':
#         fm_form = FamilyMemberForm(request.POST or None)
#         if fm_form.is_valid():
#             family_member = fm_form.save(commit=False)
#             family_member.participant = participant
#             family_member.save()
#             return redirect('hawan:view_page')
#     else:
#         fm_form = FamilyMemberForm()
#     context = {
#         'fm_form':FamilyMemberForm(),
#         'participant': participant,
#     }
#     return render(request, 'partials/add_family_form.html',context)

def letter_hawan_current(request,participant_id):
    participant = get_object_or_404(Participant, id=participant_id)
    context = {
        'participant':participant,
    }
    return render(request, 'hawan/letter_hawan.html',context)

def add_participant_with_family_members(request):
    ParticipantFormSet = inlineformset_factory(Participant, FamilyMember, fields=('name', 'gender', 'age'))
    
    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST)
        formset = ParticipantFormSet(request.POST)
        
        if participant_form.is_valid() and formset.is_valid():
            participant = participant_form.save()
            formset.instance = participant
            formset.save()
            return redirect('hawan:add_participant_with_family_members')  # Redirect to the view page
            
    else:
        participant_form = ParticipantForm()
        formset = ParticipantFormSet()
        
    context = {
        'participant_form': participant_form,
        'formset': formset,
    }
    return render(request, 'hawan/add_participant_with_family_members.html', context)
