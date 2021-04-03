from copy import deepcopy
from io import StringIO
from lxml.etree import ElementTree, Element
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

ODT_BINARY = "libreoffice"

OD_TEXT_NS = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"

OD_NSMAP = {"text": OD_TEXT_NS}
FIELD_XPATH = "//text:user-field-get"


def create_temporary_copy(path):
    tempDesc, temp_path = tempfile.mkstemp(suffix=".odt")
    os.close(tempDesc)
    shutil.copy2(path, temp_path)
    return temp_path


class ODTTemplate(object):
    def __init__(self, filename):
        # first create a temporary copy of the template
        self.tempCopy = create_temporary_copy(filename)
        self.zipfile = zipfile.ZipFile(self.tempCopy, "a")

        # extract the content and parse xml tree
        content = self.zipfile.open("content.xml", "r")
        self.tree = ElementTree()
        self.tree.parse(content)

        self.usedVariables = set()
        self.unknownVariables = set()
        self.rendered = False

    def render(self, context):
        if self.rendered:
            raise RuntimeError("You may only render the template once")

        # create matcher expressions for simple and multiline keywords
        for elem in self.tree.xpath(FIELD_XPATH, namespaces=OD_NSMAP):
            self._field_render(elem, context)

        self.render_warnings = []
        if len(self.unknownVariables) > 0:
            self.render_warnings.append(
                "The following variables occurred in the template but were not provided in the context: {}".format(
                    ",".join(self.unknownVariables)
                )
            )
        unused = set(context.keys()) - self.usedVariables
        if len(unused) > 0:
            self.render_warnings.append(
                "The following variables where not used: {}".format(",".join(unused))
            )

        # write out result to temporary archive
        outbuf = StringIO()
        self.tree.write(outbuf, encoding="utf8", xml_declaration=True)
        self.zipfile.writestr("content.xml", outbuf.getvalue())
        self.zipfile.close()
        self.rendered = True

    def debugSave(self, target):
        with open(target, "w") as f:
            self.tree.write(f, pretty_print=True, encoding="utf8", xml_declaration=True)

    def saveODT(self, target):
        if not self.rendered:
            raise RuntimeError("You cannot save an unrendered template")
        shutil.copy2(self.tempCopy, target)

    def getTemporaryODT(self):
        if not self.rendered:
            raise RuntimeError("You cannot save an unrendered template")
        return self.tempCopy

    def getTemporaryPDF(self):
        temp = tempfile.NamedTemporaryFile()
        self.savePDF(temp.name)
        return temp

    def savePDF(self, target):
        tempdir = os.path.dirname(self.tempCopy)
        with open(os.devnull, "w") as DEVNULL:
            subprocess.call(
                [
                    ODT_BINARY,
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    tempdir,
                    self.tempCopy,
                ],
                stdout=DEVNULL,
                stderr=DEVNULL,
            )
        pdfPath = os.path.splitext(self.tempCopy)[0] + ".pdf"
        shutil.copy2(pdfPath, target)
        os.unlink(pdfPath)

    def _field_render(self, elem, context):
        # retrieve the variable name of this field
        name = elem.attrib["{{{}}}name".format(OD_TEXT_NS)]
        # check if this is in our dictionary, if not, we leave it as it is
        # but create a warning
        if not name in context.keys():
            self.unknownVariables.add(name)
            return
        # otherwise mark it as used
        self.usedVariables.add(name)
        replacement = context[name]
        parent = elem.getparent()
        idx = parent.index(elem)
        # now distinguish whether its a multi-line or a single-line content
        if not "\n" in replacement:
            # in single-line replacements we just replace this element by its replacement text
            self._replace_var_with_content(elem, parent, idx, replacement)
        else:
            replacementLines = replacement.split("\n")
            # check if we are in a listing to use listing formatter
            li = parent
            isList = False
            while li is not None:
                if li.tag == "{{{}}}list-item".format(OD_TEXT_NS):
                    isList = True
                    break
                li = li.getparent()
            if isList and self._test_listitem_empty(li):
                # we do list-style replacement
                nodes = []
                for line in replacementLines:
                    cli = deepcopy(li)
                    var = cli.xpath(FIELD_XPATH, namespaces=OD_NSMAP)
                    if len(var) > 1:
                        raise RuntimeError(
                            "Multiple fields in list replacement mode are not allowed"
                        )
                    var = var[0]
                    self._replace_elem_with_text(var, line)
                    nodes.append(cli)

                # insert newly created nodes in the list after variable field
                listNode = li.getparent()
                lIdx = listNode.index(li)
                for i, node in enumerate(nodes, start=lIdx + 1):
                    listNode.insert(i, node)
                # remove list item that contains the variable
                listNode.remove(li)
            else:
                # first we have to find the parent "p" element because we want its attributes :o)
                p = parent
                while p.tag != "{{{}}}p".format(OD_TEXT_NS):
                    p = p.getparent()
                # create a copy prototype paragraph node
                pProto = Element(p.tag, **p.attrib)
                origTail = elem.tail if elem.tail else ""
                # the first line is replaced normally here, the others are appended after the current paragraph
                self._replace_var_with_content(elem, parent, idx, replacementLines[0])

                nodes = []
                for line in replacementLines[1:]:
                    n = deepcopy(pProto)
                    n.text = line
                    nodes.append(n)
                # now we have to insert the rest after our paragraph
                pParent = p.getparent()
                pIdx = pParent.index(p)
                for i, node in enumerate(nodes, start=pIdx + 1):
                    pParent.insert(i, node)
                # we have to update the tail of the last inserted node to the tail of the variable
                last = pParent.getchildren()[pIdx + len(nodes)]
                last.text = last.text + origTail

    def _replace_elem_with_text(self, elem, text):
        parent = elem.getparent()
        idx = parent.index(elem)
        self._replace_var_with_content(elem, parent, idx, text)

    def _replace_var_with_content(self, elem, parent, idx, replacement):
        if idx == 0:
            # if we are the first child, the replacement has to be done in the parent
            tail = elem.tail if elem.tail else ""
            text = parent.text if parent.text else ""
            parent.text = text + replacement + tail
            parent.remove(elem)
        else:
            # otherwise we have to update the previous sibling
            prevSib = parent.getchildren()[idx - 1]
            prevTail = prevSib.tail if prevSib.tail else ""
            tail = elem.tail if elem.tail else ""
            prevSib.tail = prevTail + replacement + tail
            parent.remove(elem)

    def _test_listitem_empty(self, listitem):
        for elem in listitem.iterdescendants():
            if elem.tag != "{{{}}}user-field-get".format(OD_TEXT_NS) and (
                elem.text is not None or elem.tail is not None
            ):
                return False
        return True

    def __del__(self):
        if hasattr(self, "zipfile"):
            self.zipfile.close()
        if hasattr(self, "tempCopy") and len(self.tempCopy) > 0:
            os.unlink(self.tempCopy)
