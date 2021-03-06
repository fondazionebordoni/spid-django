import json
import random

from django import template
from django.conf import settings
from django.urls import reverse

from ..apps import SpidConfig

register = template.Library()

SPID_BUTTON_SIZES = {"small", "medium", "large", "xlarge"}


@register.inclusion_tag("spid_button.html", takes_context=True)
def spid_button(context, size="medium", index="0", next=None, btn_id=None):
    if size not in SPID_BUTTON_SIZES:
        raise ValueError(
            "argument 'size': value %r not in %r." % (size, SPID_BUTTON_SIZES)
        )

    spid_idp_list = [
        {"id": k, "name": v["name"]}
        for k, v in SpidConfig.identity_providers_spid.items()
    ]
    random.shuffle(spid_idp_list)
    result = {
        "method": context["request"].method.lower(),
        "post_data": context["request"].POST,
        "spid_button_size": size,
        "index": index,
        "spid_button_size_short": size[0] if size != "xlarge" else size[:2],
        "spid_idp_list": spid_idp_list,
        "btn_id": btn_id,
    }
    if next:
        result["next"] = reverse(next)
    return result


@register.inclusion_tag("eid_button.html", takes_context=True)
def eid_button(context, idp_id="eid_test", size="medium", index="1", next=None, btn_id=None):
    if size not in SPID_BUTTON_SIZES:
        raise ValueError(
            "argument 'size': value %r not in %r." % (size, SPID_BUTTON_SIZES)
        )
    result = {
        "method": context["request"].method.lower(),
        "post_data": context["request"].POST,
        "spid_button_size": size,
        "index": index,
        "idp_id": idp_id,
        "spid_button_size_short": size[0] if size != "xlarge" else size[:2],
        "btn_id": btn_id
    }
    if next:
        result["next"] = reverse(next)
    return result


@register.simple_tag
def idp_list():
    return json.dumps(
        [
            {"id": k, "name": v["name"]}
            for k, v in SpidConfig.identity_providers_spid.items()
        ]
    )
