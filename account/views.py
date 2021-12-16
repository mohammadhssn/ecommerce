from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy

from .forms import RegistrationForm, UserLoginForm, UserEditForm, PwdResetForm, PwdReseConfirmForm, UserAddressForm
from .models import Customer, Address
from .token import account_activation_token
from orders.views import UserOrders


class AccountRegister(View):
    from_class = RegistrationForm
    template_name = 'account/registration/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': self.from_class})

    def post(self, request):
        form = self.from_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            # Setup email
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/register_email_confirm.html', {'form': form})
        return render(request, self.template_name, {'form': form})


class AccountActivate(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Customer.objects.get(pk=uid)
        except():
            pass
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('account:dashboard')
        else:
            return render(request, 'account/registration/activation_invalid.html')


class AccountLogin(auth_view.LoginView):
    template_name = 'account/login.html'
    form_class = UserLoginForm


class AccountLogout(LoginRequiredMixin, auth_view.LogoutView):
    next_page = '/account/login/'


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        orders = UserOrders.get(self, request)
        return render(request, 'account/dashboard/dashboard.html', {'orders': orders})


class EditProfile(LoginRequiredMixin, View):
    form_class = UserEditForm
    template_name = 'account/dashboard/edit_detail.html'

    def get(self, request):
        user_form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'user_form': user_form})

    def post(self, request):
        user_form = self.form_class(data=request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('account:dashboard')
        return render(request, self.template_name, {'user_form': self.form_class(instance=request.user)})


class DeleteUser(LoginRequiredMixin, View):

    def post(self, request):
        user = get_object_or_404(Customer, name=request.user)
        user.is_active = False
        user.save()
        logout(request)
        return redirect('account:delete_confirmation')


# Password Resset
class UserPassReset(auth_view.PasswordResetView):
    template_name = 'account/password_reset/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset/password_reset_email.html'
    form_class = PwdResetForm


class UserPassResetDone(auth_view.PasswordResetDoneView):
    template_name = 'account/password_reset/reset_status.html'


class UserPassResetConfirm(auth_view.PasswordResetConfirmView):
    template_name = 'account/password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')
    form_class = PwdReseConfirmForm


class UserPassResetComplete(auth_view.PasswordResetCompleteView):
    template_name = 'account/password_reset/reset_status.html'


# Addresses

class ViewAddress(LoginRequiredMixin, View):

    def get(self, request):
        addresses = Address.objects.filter(customer=request.user)
        return render(request, 'account/dashboard/addresses.html', {'addresses': addresses})


class AddAddress(LoginRequiredMixin, View):
    form_class = UserAddressForm
    template_name = 'account/dashboard/edit_addresses.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.customer = request.user
            form.save()
            return redirect('account:addresses')
        return render(request, self.template_name, {'form': form})


class EditeAddress(LoginRequiredMixin, View):
    template_name = 'account/dashboard/edit_addresses.html'
    form_class = UserAddressForm

    def setup(self, request, *args, **kwargs):
        self.address = get_object_or_404(Address, pk=kwargs.get('id'), customer=request.user)
        super().setup(request, *args, **kwargs)

    def get(self, request, **kwargs):
        form = self.form_class(instance=self.address)
        return render(request, self.template_name, {'form': form})

    def post(self, request, **kwargs):
        form = self.form_class(data=request.POST, instance=self.address)
        if form.is_valid():
            form.save()
            return redirect('account:addresses')
        return render(request, self.template_name, {'form': form})


class DeleteAddress(LoginRequiredMixin, View):

    def get(self, request, id):
        address = get_object_or_404(Address, pk=id, customer=request.user)
        address.delete()
        return redirect('account:addresses')


class SetDefaultAddress(LoginRequiredMixin, View):

    def get(self, request, id):
        Address.objects.filter(customer=request.user, default=True).update(default=False)
        Address.objects.filter(pk=id, customer=request.user).update(default=True)
        return redirect('account:addresses')
