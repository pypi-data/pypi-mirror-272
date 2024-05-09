from zenui.tags import Element, Child, Attribute
from zenui.compiler import ZenuiCompiler
import unittest

class ZenuiCompilerTests(unittest.TestCase):
    def test_compile_simple_element(self):
        elm = Element("div")
        compiler = ZenuiCompiler()
        result = compiler.compile(elm)
        self.assertEqual(result, "<div></div>")

    def test_compile_with_attributes(self):
        elm = Element("p")
        elm.children.append(Attribute("styles", "my-paragraph"))
        elm.children.append(Attribute("id", "main-content"))
        compiler = ZenuiCompiler()
        result = compiler.compile(elm)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    
    def test_compile_with_attributes(self):
        elm = Element("p")
        elm.attributes.append(Attribute("styles", "my-paragraph"))
        elm.attributes.append(Attribute("id", "main-content"))
        compiler = ZenuiCompiler()
        result = compiler.compile(elm)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    def test_compile_with_attributes(self):
        elm = Element("p")
        elm.attributes.append(Attribute("styles", "my-paragraph"))
        elm.attributes.append(Attribute("id", "main-content"))
        compiler = ZenuiCompiler()
        result = compiler.compile(elm)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    def test_compile_with_children(self):
        div = Element("div")
        span = Element("span", [])
        span.children.append(Element(name="text",children=["Hello"]))
        div.children.append(span)
        compiler = ZenuiCompiler()
        result = compiler.compile(div)
        self.assertEqual(result, "<div><span>Hello</span></div>")

    def test_process_attributes(self):
        attrs = [Attribute("id", "my-element"), Attribute("styles", "important")]
        compiler = ZenuiCompiler()
        result = compiler.process_attributes(attrs)
        #  note here space is important <div id=....
        self.assertEqual(result, ' id="my-element" class="important"')

    