from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from .models import *
from .models import Post
from .models import GoalType
from .forms import GoalForm



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content'] 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content'] 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def menu(request):
    return render(request, 'blog/dropmenu.html')

def news(request):

    news_api_request = requests.get("http://newsapi.org/v2/everything?q=bitcoin&from=2020-03-13&sortBy=publishedAt&apiKey=aee04ffc13154e69a54004c264ace2c7")
    api = json.loads(news_api_request.content)

    return render(request, 'blog/news.html', {'api': api})

from django.db.models.functions import TruncMonth, TruncYear
from django.conf import settings

from itertools import chain
from dateutil.relativedelta import relativedelta
import datetime
CURRENCY = '$'


class BudgetView(TemplateView):
    template_name = 'blog/budget_view.html'

    def get_context_data(self, **kwargs):
        context = super(BudgetView, self).get_context_data(**kwargs)
        bills = Bill.my_query.get_queryset().unpaid()[:10]
        payrolls = Payroll.my_query.get_queryset().unpaid()[:10]
        expenses = GenericExpense.my_query.get_queryset().unpaid()[:10]
        context.update({'bills': bills,
                        'payroll': payrolls,
                        'expenses': expenses
                        })
        return context


class BillListView(ListView):
    model = Bill
    template_name = 'blog/page_list.html'
    paginate_by = 100

    def get_queryset(self):
        queryset = Bill.objects.all()
        queryset = Bill.filters_data(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BillListView, self).get_context_data(**kwargs)
        page_title = 'Bills List'
        categories = BillCategory.objects.all()
        search_name, cate_name, paid_name = [self.request.GET.get('search_name', None),
                                             self.request.GET.getlist('cate_name', None),
                                             self.request.GET.getlist('paid_name', None)
                                             ]
        total_value, paid_value, diff, category_analysis = Bill.analysis(self.object_list)
        currency = CURRENCY
        context.update(locals())
        return context


class PayrollListView(ListView):
    model = Payroll
    template_name = 'blog/page_list.html'
    paginate_by = 100

    def get_queryset(self):
        queryset = Payroll.objects.all()
        queryset = Payroll.filters_data(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PayrollListView, self).get_context_data(**kwargs)
        page_title = 'Revenue List'
        categories = PayrollCategory.objects.all()
        persons = Person.objects.all()
        search_name, cate_name, paid_name, person_name = [self.request.GET.get('search_name', None),
                                                          self.request.GET.getlist('cate_name', None),
                                                          self.request.GET.getlist('paid_name', None),
                                                          self.request.GET.getlist('person_name', None)
                                                          ]
        total_value, paid_value, diff, category_analysis = Payroll.analysis(self.object_list)
        currency = CURRENCY
        context.update(locals())
        return context


class ExpensesListView(ListView):
    model = GenericExpense
    template_name = 'blog/page_list.html'
    paginate_by = 100

    def get_queryset(self):
        queryset = GenericExpense.objects.all()
        queryset = GenericExpense.filters_data(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ExpensesListView, self).get_context_data(**kwargs)
        page_title = 'Expenses List'
        categories = GenericExpenseCategory.objects.all()
        search_name, cate_name, paid_name = [self.request.GET.get('search_name', None),
                                             self.request.GET.getlist('cate_name', None),
                                             self.request.GET.getlist('paid_name')
                                             ]
        total_value, paid_value, diff, category_analysis = GenericExpense.analysis(self.object_list)
        currency = CURRENCY
        context.update(locals())
        return context


def report_view(request):
    startDate = request.GET.get('startDate', '2020-01-01')
    endDate = request.GET.get('endDate', '2020-12-31')
    if startDate > endDate:
        startDate , endDate = '2020-01-01', '2020-12-31'
    date_start = datetime.datetime.strptime(startDate, '%Y-%m-%d').date()
    date_end = datetime.datetime.strptime(endDate, '%Y-%m-%d').date()
    bills = Bill.my_query.get_queryset().filter_by_date(date_start, date_end)
    payrolls = Payroll.my_query.get_queryset().filter_by_date(date_start, date_end)
    expenses = GenericExpense.my_query.get_queryset().filter_by_date(date_start, date_end)
    queryset = sorted(chain(bills, payrolls, expenses),
                    key=lambda instance: instance.date_expired
                    )
    bill_total_value, bill_paid_value, bill_diff, bill_category_analysis = DefaultExpenseModel.analysis(bills)
    payroll_total_value, payroll_paid_value, payroll_diff, bill_category_analysis = DefaultExpenseModel.analysis(payrolls)
    expense_total_value, expense_paid_value, expense_diff, expense_category_analysis = DefaultExpenseModel.analysis(expenses)

    bill_by_month, payroll_by_month, expenses_by_month, totals_by_month = [], [], [],[]
    months_list = []
    while date_start < date_end:
        months_list.append(date_start)
        date_start += relativedelta(months=1)

    for date in months_list:
        start = date.replace(day=1)
        next_month = date.replace(day=28) + datetime.timedelta(days=4)
        days = int(str(next_month).split('-')[-1])
        end = next_month - datetime.timedelta(days=days)
        print(next_month, end)
        this_month_bill_queryset = bills.filter(date_expired__range=[start, end])
        this_month_bills = DefaultExpenseModel.analysis(this_month_bill_queryset)
        this_month_payroll_queryset = payrolls.filter(date_expired__range=[start, end])
        this_month_payroll = DefaultExpenseModel.analysis(this_month_payroll_queryset)
        this_month_expense_queryset = expenses.filter(date_expired__range=[start, end])
        this_month_expense = DefaultExpenseModel.analysis(this_month_expense_queryset)
        bill_by_month.append(this_month_bills)
        payroll_by_month.append(this_month_expense)
        expenses_by_month.append(this_month_payroll)
        totals_by_month.append([this_month_bills[0]+this_month_expense[0]+ this_month_payroll[0],
                                this_month_bills[1] + this_month_expense[1] + this_month_payroll[1],
                                this_month_bills[2] + this_month_expense[2] + this_month_payroll[2]
                                ])

    totals = [payroll_total_value + bill_total_value + expense_total_value,
              bill_paid_value + payroll_paid_value + expense_paid_value,
              bill_diff + payroll_diff + expense_diff
              ]
    currency = CURRENCY
    context = locals()
    return render(request, 'blog/report.html', context=context)


def goal_entry(request):#, id = None):
    title1 = 'List of all goals entered'
    queryset = GoalType.objects.all()
    title2 = 'Add Goal'
    form = GoalForm(request.POST or None)
    if form.is_valid():
        form.save()

    '''instance = get_list_or_404(GoalType, id=id )
    form = GoalForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('/goals')'''

    context = {
        "title1":title1,
        "queryset":queryset,
        "title2": title2,
        #"title": 'Edit ' + str(instance.goal_objectives),
        #"instance": instance,
        "form": form,
    }
    return render(request, "blog/goals.html",context)
