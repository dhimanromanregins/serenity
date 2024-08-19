from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from book_management.models import Book
from .models import Review
from .forms import ReviewForm


@login_required
def submit_review(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = ReviewForm()
    return render(request, 'reviews_management/review_form.html', {'form': form, 'book': book})

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews_management/review_form.html'
    success_url = reverse_lazy('book_list')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews_management/review_confirm_delete.html'
    success_url = reverse_lazy('book_list')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
