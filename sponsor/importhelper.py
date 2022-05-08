# this is a helper script to import sponsor contacts from the old redmine plugin

from lxml import etree
from models import SponsorContact, SponsorMailTemplate
import re

addrRe = re.compile("([^\n]+\d+[^\n]*)\n(\d+)\s+([^\n]+)", re.M)
csvRe = re.compile("([^\t]+)\t+(DE|EN), (M|F) ([^(]+) \\(([^)]+)\\) <(.*)>")

# load an anymous template and a personal template
anonymous_template = SponsorMailTemplate.objects.get(
    templateName="sponsor/mails/DamenUndHerren.html"
)
personal_template = SponsorMailTemplate.objects.get(
    templateName="sponsor/mails/Sie.html"
)
du_template = SponsorMailTemplate.objects.get(templateName="sponsor/mails/Du.html")


def load_contacts_xml(filename):
    t = etree.parse(filename)
    # already filter away all that we cannot use
    return t.xpath("/contacts/contact[company!='' and emails]")


def xml_gettext_if_exists(node, childname, default=""):
    c = node.find(childname)
    if c is None:
        return default
    if c.text is None:
        return default
    return c.text.strip()


def contactFromCSVLine(line):
    res = csvRe.match(line)
    if res is None:
        return None

    c = SponsorContact()
    c.companyName = res.group(1)
    c.street = "(unknown)"
    c.zipcode = "0"
    c.city = "(unknown)"
    c.contactEMail = res.group(6)
    c.contactPersonFirstname, c.contactPersonSurname = res.group(4).split(" ")
    c.contactPersonEmail = res.group(6)
    c.contactPersonGender = res.group(3)

    c.comment = "!!! Automatically imported contact !!!"
    if c.contactPersonFirstname == res.group(5):
        c.template = du_template
    elif res.group(5).startswith("Herr") or res.group(5).startswith("Frau"):
        c.template = personal_template
    else:
        c.comment = (
            c.comment
            + "\nContact detail was: "
            + res.group(4)
            + " with form of address "
            + res.group(5)
        )
        c.template = anonymous_template
    return c


def contactFromXMLContact(node):
    c = SponsorContact()
    c.companyName = node.find("company").text.strip()
    emails = node.xpath("emails/email/address")
    if len(emails) == 0:
        return None
    c.contactEMail = emails[0].text.strip()
    # try to parse address
    addr = xml_gettext_if_exists(node, "address")
    res = addrRe.match(addr)
    if res:
        c.street = res.group(1).strip()
        c.zipcode = res.group(2)
        c.city = res.group(3).strip()
    else:
        # these fields are obligatory
        c.street = "(unknown)"
        c.zipcode = "0"  # zipcode is char field
        c.city = "(unknown)"

    lnNode = node.find("last_name")
    if lnNode is not None and lnNode.text is not None and len(lnNode.text.strip()) > 0:
        fn = xml_gettext_if_exists(node, "first_name")
        sn = lnNode.text.strip()
        c.contactPersonFirstname = fn
        c.contactPersonSurname = sn
        c.template = personal_template
    else:
        c.template = anonymous_template

    bground = xml_gettext_if_exists(node, "background", default="(empty)")
    tags = xml_gettext_if_exists(node, "tag_list", default="(empty)")
    c.comment = (
        "!!! Automatically imported contact !!!\nImported comment:\n"
        + bground
        + "\nOld Tags\n"
        + tags
    )
    return c


def checkDoubleContact(c):
    res = []
    # find by company name
    q = SponsorContact.objects.filter(companyName__iexact=c.companyName)
    if len(q) > 0:
        res.extend(list(q))
    # find by general mail
    q = SponsorContact.objects.filter(contactEMail__iexact=c.contactEMail)
    if len(q) > 0:
        res.extend(list(q))
    if c.contactPersonEmail != "":
        q = SponsorContact.objects.filter(contactEMail__iexact=c.contactPersonEmail)
        if len(q) > 0:
            res.extend(list(q))
    # find by contact person mail
    if c.contactPersonEmail != "":
        q = SponsorContact.objects.filter(
            contactPersonEmail__iexact=c.contactPersonEmail
        )
        if len(q) > 0:
            res.extend(list(q))
    q = SponsorContact.objects.filter(contactPersonEmail__iexact=c.contactEMail)
    if len(q) > 0:
        res.extend(list(q))

    return list(set(res))


def saveIfDoubleAsk(cList):
    for c in cList:
        doubles = checkDoubleContact(c)
        if len(doubles) > 0:
            print("{} collides with {}, override?".format(c, doubles))
            inp = raw_input("y/n")
            if inp != "y":
                continue
            for d in doubles:
                d.delete()
        c.save()
