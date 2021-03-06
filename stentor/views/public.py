# -*- coding: utf-8 -*-
# TODO: Check this module thoroughly.
"""
The views for all public facing urls of the application.
"""
from __future__ import unicode_literals

import importlib

from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.template import Template, Context
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from django.views.generic import FormView, TemplateView

try:
    from django.urls import reverse_lazy, resolve
except ImportError:  # NOTE: Deprecation -- django < 2
    from django.core.urlresolvers import reverse_lazy, resolve

from .. import settings as stentor_conf
from ..utils import obfuscator

from ..models import Newsletter, Subscriber


TRANSPARENT_1_PIXEL_GIF = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'  # NOQA


class AjaxTemplateMixin(object):
    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        return [self.template_name]


class SubscriptionHandlingMixin(object):
    def form_valid(self, form):
        response = super(SubscriptionHandlingMixin, self).form_valid(form)
        form.save()
        if self.request.is_ajax():
            # Fetch the template from the view that handles successful
            # submissions of this view redirect to.
            view_func = resolve(self.get_success_url()).func
            module = importlib.import_module(view_func.__module__)
            view = getattr(module, view_func.__name__)
            template = view.ajax_template_name

            html = render_to_string(
                template,
                {'form': form},
                self.request
            )
            data = {
                'success': True,
                'html': html,
                'errors': form.errors  # should be empty
            }
            return JsonResponse(data)
        return response

    def form_invalid(self, form):
        response = super(SubscriptionHandlingMixin, self).form_invalid(form)
        if self.request.is_ajax():
            html = render_to_string(
                self.get_template_names(),
                {'form': form},
                self.request
            )
            data = {
                'success': False,
                'html': html,
                'errors': form.errors,
            }
            return JsonResponse(data)
        return response


class SubscribeSuccessView(AjaxTemplateMixin, TemplateView):
    template_name = 'stentor/subscribe_success.html'
    ajax_template_name = 'stentor/partials/subscribe_success_message.html'


class SubscribeView(AjaxTemplateMixin, SubscriptionHandlingMixin, FormView):
    form_class = import_string(stentor_conf.SUBSCRIBE_FORM)
    success_url = reverse_lazy('stentor:subscriber.subscribe_success')
    template_name = 'stentor/subscribe.html'
    ajax_template_name = 'stentor/partials/subscribe_form.html'

    def get_context_data(self, **kwargs):
        out = super(SubscribeView, self).get_context_data(**kwargs)
        out['stentor_subscribe_form'] = out['form']
        return out


class UnsubscribeSuccessView(AjaxTemplateMixin, TemplateView):
    template_name = 'stentor/unsubscribe_success.html'
    ajax_template_name = 'stentor/partials/unsubscribe_success_message.html'


class UnsubscribeView(AjaxTemplateMixin, SubscriptionHandlingMixin, FormView):
    form_class = import_string(stentor_conf.UNSUBSCRIBE_FORM)
    success_url = reverse_lazy('stentor:subscriber.unsubscribe_success')
    template_name = 'stentor/unsubscribe.html'
    ajax_template_name = 'stentor/partials/unsubscribe_form.html'

    def dispatch(self, request, *args, **kwargs):
        out = super(UnsubscribeView, self).dispatch(request, *args, **kwargs)
        ord_day_created, subscriber_pk = obfuscator.decode_unsubscribe_hash(
            self.kwargs['unsubscribe_hash']
        )
        subscriber = get_object_or_404(Subscriber, pk=subscriber_pk)
        if ord_day_created != str(subscriber.creation_date.toordinal()):
            raise Http404()
        return out

    def get_context_data(self, **kwargs):
        out = super(UnsubscribeView, self).get_context_data(**kwargs)
        out['stentor_unsubscribe_form'] = out['form']
        return out

    def get_initial(self):
        initial = {
            'unsubscribe_hash': self.kwargs['unsubscribe_hash']
        }
        if 'newsletter_hash' in self.kwargs:
            initial['newsletter_hash'] = self.kwargs['newsletter_hash']
        return initial


def _newsletter_web_view(request, newsletter_slug, subscriber=None):
    newsletter = get_object_or_404(Newsletter, slug=newsletter_slug)
    newsletter.add_impression(subscriber, 'web')
    context_vars = {
        'newsletter': newsletter,
        'subscriber': subscriber,
    }
    template = Template(newsletter.web_html)
    context = Context(context_vars)
    output = template.render(context)
    return HttpResponse(output)


def newsletter_web_view_from_subscriber(
        request, newsletter_slug, subscriber_hash):
    __, subscriber_pk = obfuscator.decode_web_view_hash(subscriber_hash)
    subscriber = get_object_or_404(Subscriber, pk=subscriber_pk)
    return _newsletter_web_view(request, newsletter_slug, subscriber)


def newsletter_web_view_from_anonymous(request, newsletter_slug):
    return _newsletter_web_view(request, newsletter_slug)


def newsletter_email_tracker(request, newsletter_slug, subscriber_hash):
    newsletter = get_object_or_404(Newsletter, slug=newsletter_slug)
    __, subscriber_pk = obfuscator.decode_email_tracker_hash(subscriber_hash)
    subscriber = get_object_or_404(Subscriber, pk=subscriber_pk)
    newsletter.add_impression(subscriber, 'email')
    return HttpResponse(TRANSPARENT_1_PIXEL_GIF, content_type="image/gif")
