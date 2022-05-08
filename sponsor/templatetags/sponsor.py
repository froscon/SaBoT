from django import template

register = template.Library()

color_class_table = {
    -2: "",
    -1: "icon-na",
    0: "icon-danger",
    1: "icon-warning",
    2: "icon-success",
}


@register.filter(name="statuscolorclass")
def statuscolorclass(value):
    return color_class_table.get(value, "")


@register.filter(name="xsddatetime")
def xsddatetime(value):
    return value.strftime("%Y-%m-%dT%H:%M:%S")


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).count() > 0
