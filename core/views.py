from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.utils import timezone
from .forms import *
from .models import *
from django.http import HttpResponseRedirect
# from django.shortcuts import render_to_response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from itertools import chain
from operator import attrgetter
from django.views.generic import TemplateView
from django.core.mail import send_mail, BadHeaderError, mail_admins
from django.urls import reverse_lazy, reverse
# Create your views here.
import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def makertplace(request):
    pass

def aide(request):
    pass

@login_required
def myboutiks(request):
    pass

@login_required
def myproducts(request):
    pass

def boutiks(request):
    boutiks = Boutique.objects.all()
    return render(request, 'boutiks.html', {'boutiks': boutiks})

def boutik_detail(request, year, month, day, boutik):
    boutik = get_object_or_404(Boutique, slug=boutik)
    items = boutik.items.filter(is_active=True)

    print (items)

    return render(request,
        'boutik_detail.html',
        {'boutik': boutik,
        'items': items
        })
    
    
class AddBoutikView(LoginRequiredMixin, CreateView):
    model = Boutique
    success_url = reverse_lazy('core:myboutiks')
    template_name = 'sellers/addboutiks.html'
    form_class = BoutikForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        boutik = self.get_object()
        if self.request.user == boutik.author:
            return True
        return False

class BoutikUpdateView(LoginRequiredMixin, UpdateView):
    model = Boutique
    template_name = 'sellers/addboutiks.html'
    success_url = reverse_lazy('core:myboutiks')
    form_class = BoutikForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        boutik = self.get_object()
        if self.request.user == boutik.author:
            return True
        return False
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(author=self.request.user)

class BoutikDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'boutik_delete.html'
    model = Boutique
    success_url = reverse_lazy('core:myboutiks')
    
class AddProductView(LoginRequiredMixin, CreateView):
    model = ItemSeller
    success_url = reverse_lazy('core:myprods')
    template_name = 'sellers/addproducts.html'
    form_class = ItemForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        boutik = self.get_object()
        if self.request.user == boutik.author:
            return True
        return False


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = ItemSeller
    template_name = 'sellers/addproducts.html'
    success_url = reverse_lazy('core:myprods')
    form_class = ItemForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        boutik = self.get_object()
        if self.request.user == boutik.author:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'product_delete.html'
    model = ItemSeller
    success_url = reverse_lazy('core:myprods')

@login_required
def profile(request):
    return render(request, 'sellers/profile.html' )

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'sellers/profile_update.html'

    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'votre profile est mise-a-jour')
            return HttpResponseRedirect(reverse_lazy('core:profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        # return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def contact(request):
    if request.method == 'POST':
        f = ContactusForm(request.POST)
        if f.is_valid():
            name = f.cleaned_data['name']
            sender = f.cleaned_data['email']
            subject = "You have a new message from {}:{}".format(name, sender)
            message = "Subject: {}\n\nMessage: {}".format(f.cleaned_data['subject'], f.cleaned_data['message'])
            mail_admins(subject, message)

            f.save()
            messages.add_message(request, messages.INFO, 'votre message a été envoyer avec success.')
            return redirect('contact')
    else:
        f = ContactusForm()
    return render(request, 'contact.html', {'form': f})


def about(request):
    return render(request, 'about.html')

class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, "checkout.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            print(self.request.POST)
            if form.is_valid():
                quartier_addresse = form.cleaned_data.get('quartier_addresse')
                apartment_addresse = form.cleaned_data.get('apartment_addresse')
                pays = form.cleaned_data.get('pays')
                zip = form.cleaned_data.get('zip')
                city = form.cleaned_data.get('city')
                # add functionality for these fields
                # same_shipping_address = form.cleaned_data.get(
                #     'same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    quartier_addresse=quartier_addresse,
                    apartment_addresse=apartment_addresse,
                    pays=pays,
                    zip=zip,
                    city=city,
                    address_type='B'
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
 
                # add redirect to the selected payment option
                if payment_option == 'S':
                    return redirect('core:payment_cc')
                elif payment_option == 'P':
                    return redirect('core:payment_paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option select")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:order-summary",)


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

def payment_paypal(request):
    order_id = request.session.get('order_id')
    # order = get_object_or_404(Order, id=order_id)
    order = Order.objects.get(user=request.user)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % int(order.get_total()),
        # 'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse_lazy('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse_lazy('core:payment_p_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse_lazy('core:payment_p_canceled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment-p.html', {'order': order, 'form': form})    

@csrf_exempt
def payment_p_done(request):
    order = Order.objects.get(user=request.user, ordered=False)
    # assign the payment to the order
    order.ordered = True
    # TODO : assign ref code
    order.ref_code = create_ref_code()
    order.save()

    messages.success(request, "Order was successful")
    return render(request, 'payment-paypal-done.html')

@csrf_exempt
def payment_p_canceled(request):
    return render(request, 'payment-paypal-cancelled.html')

def order_view(request):
    """
    Render thank you page with order number,
    after transaction is made.
    """
    # order_id = request.session['order_id']
    order = Order.objects.get(user=request.user, ordered=True)
    context = {
        'order': order,
    }
    return render(request, 'order_view.html', context)

class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        # order
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "u have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total())
        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )
            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order
            order.ordered = True
            order.payment = payment
            # TODO : assign ref code
            order.ref_code = create_ref_code()
            order.save()

            messages.success(self.request, "Order was successful")
            return redirect("/")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "RateLimitError")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Not Authentication")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network Error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.error(self.request, "Serious Error occured")
            return redirect("/")


def home(request):
    boutiks = Boutique.objects.all()
    produit1_slide = Item.objects.all()[:4]
    produit2_slide = ItemSeller.objects.all()[:4]
    prodres = sorted(chain(produit1_slide,produit2_slide), key=attrgetter('price'))
    produit1 = Item.objects.all()[:6]
    produit2 = ItemSeller.objects.all()[:6]
    items = sorted(chain(produit1,produit2), key=attrgetter('title'))
    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context = {
        'items': items,
        'paginate': True
    }
    return render(request, 'index.html', {'items': items, 'boutiks': boutiks, 'prodres':prodres})


@login_required
def itemse_detail(request, year, month, day, itemse):
    itemse = get_object_or_404(ItemSeller, slug=itemse)
    return render(request,'itemse_detail.html',
        {'itemse': itemse})

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/") 


def shop(request):
    produit1 = Item.objects.all()
    produit2 = ItemSeller.objects.all()
    items = sorted(chain(produit1,produit2), key=attrgetter('title'))
    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context = {
        'items': items,
        'paginate': True
    }
    return render(request, 'shop.html', {'items': items})


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-detail.html"


# class CategoryView(DetailView):
#     model = Category
#     template_name = "category.html"

class CategoryView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        item = Item.objects.filter(category=category, is_active=True)
        context = {
            'object_list': item,
            'category_title': category,
            'category_description': category.description,
            'category_image': category.image
        }
        return render(self.request, "category.html", context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item qty was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to your cart.")
    return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "Item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "Item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "u don't have an active order.")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item qty was updated.")
            return redirect("core:order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "Item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "u don't have an active order.")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")

            except ObjectDoesNotExist:
                messages.info(request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist")
                return redirect("core:request-refund")
