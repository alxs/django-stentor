# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings


# A list of callables that modify the context of a Newsletter's renders. These
# handlers take a dictionary as the first argument (the "base" context of the
# render) and a string argument that signifies the nature of the render
# ('email_html' and 'web_html' for the moment). They should all return a
# dictionary (empty or not).
CONTEXT_HANDLERS = getattr(
    settings,
    'STENTOR_CONTEXT_HANDLERS',
    []
)

DEFAULT_MAILING_LISTS = getattr(
    settings,
    'STENTOR_DEFAULT_MAILING_LISTS',
    ['Website subscribers']
)

EXTRA_HEADERS = getattr(
    settings,
    'STENTOR_EXTRA_HEADERS',
    {}
)

OBFUSCATION_BACKEND = getattr(
    settings,
    'STENTOR_OBFUSCATION_BACKEND',
    'stentor.obfuscation.dummy.backend'
)

OBFUSCATION_SETTINGS = getattr(
    settings,
    'STENTOR_OBFUSCATION_SETTINGS',
    {}
)

# STENTOR_SLUGIFY has the following possible values:
#   - If set to None, no slugify will take place.
#   - If "falsy", but not None, django.utils.text.slugify will be used with
#     the newsletter subject as input and allow_unicode set to False.
#   - If it's "truthy", the value will be assumed to be a callable and it will
#     be passed the Newsletter instance, so account for it.
SLUGIFY = getattr(
    settings,
    'STENTOR_SLUGIFY',
    False
)

# The "base" URL that will serve the tracking image of newsletters, their web
# views and the unsubscription of Subscribers.
# NOTE: If this is not set, stentor tries to get the url from the current Site,
# as given by the django.contrib.sites app.
PUBLIC_SITE_URL = getattr(
    settings,
    'STENTOR_PUBLIC_SITE_URL',
    ''
)

# This is used in cases where the "admin/cms site", where the creation of
# newsletters takes place, is different than the "public site" where web
# views of newsletters take place.
PUBLIC_URLCONF = getattr(
    settings,
    'STENTOR_PUBLIC_URLCONF',
    settings.ROOT_URLCONF
)

# TODO: Is this used or needed as it is now? Change the default to an empty
# string for disabling it.
REPLY_TO = getattr(
    settings,
    'STENTOR_REPLY_TO',
    ()
)

SENDER_EMAIL = getattr(
    settings,
    'STENTOR_SENDER_EMAIL',
    settings.DEFAULT_FROM_EMAIL
)

SENDER_NAME = getattr(
    settings,
    'STENTOR_SENDER_NAME',
    ''
)

SCHEDULED_SENDING_BATCH_SIZE = getattr(
    settings,
    'STENTOR_SCHEDULED_SENDING_BATCH_SIZE',
    250
)


# An iterable of strings, representing paths to callables that accept a
# collection of Subscribers and a Newsletter instance and return a collection
# of Subscribers. This can be used to filter the Subscribers that will
# receive a Newsletter.
SCHEDULABLE_RECIPIENTS_PROCESSORS = getattr(
    settings,
    'STENTOR_SCHEDULABLE_RECIPIENTS_PROCESSORS',
    ()
)


if SENDER_NAME:
    SENDER_VERBOSE = '{} <{}>'.format(SENDER_NAME, SENDER_EMAIL)
else:
    SENDER_VERBOSE = SENDER_EMAIL

SUBSCRIBE_FORM = getattr(
    settings,
    'STENTOR_SUBSCRIBE_FORM',
    'stentor.forms.SubscribeForm'
)


# If this evaluates to True, then a subscription confirmation email will be
# sent to all new Subscribers.
# NOTE: Setting this to a truthy value will require of you to create a
# `stentor/subscribe_confirmation_email.html` template as well. Stentor does
# not provide this.
# TODO: Add a check that looks for the existence of the template.
SUBSCRIPTION_CONFIRMATION = getattr(
    settings,
    'STENTOR_SUBSCRIPTION_CONFIRMATION',
    False
)


# If SUBSCRIPTION_CONFIRMATION is truthy, the subject of the confirmation
# email will be this value.
SUBSCRIPTION_CONFIRMATION_SUBJECT = getattr(
    settings,
    'STENTOR_SUBSCRIPTION_CONFIRMATION_SUBJECT',
    'Thank you for subscribing to our newsletter'
)

TEMPLATES = getattr(
    settings,
    'STENTOR_TEMPLATES',
    {
        'Custom': (
            'stentor/newsletter/custom_email.html',  # template for email views
            'stentor/newsletter/custom_web.html'  # template for web views
        )
    }
)

UNSUBSCRIBE_FORM = getattr(
    settings,
    'STENTOR_UNSUBSCRIBE_FORM',
    'stentor.forms.UnsubscribeForm'
)
