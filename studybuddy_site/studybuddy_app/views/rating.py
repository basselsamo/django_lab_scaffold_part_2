from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from ..forms import RatingForm
from ..models import Meetup, Rating

class RatingListView(LoginRequiredMixin, generic.ListView):
    model = Rating

class RatingDetailView(LoginRequiredMixin, generic.DetailView):
    model = Rating

@login_required
def create_rating(request, pk):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.meetup = get_object_or_404(Meetup, pk=pk)
            rating.save()
            return HttpResponseRedirect(reverse('studybuddy_app:meetup.detail', args=[pk]))
    else:
        form = RatingForm()
    return render(request, 'studybuddy_app/rating_form.html', {'form': form})
