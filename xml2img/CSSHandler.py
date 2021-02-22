from parsel import Selector
from .Element import Element

import cssselect2
import tinycss2

class CSSHandler:
    def __init__(self, path):
        self.css = open(path,'r').read()

    def get_css(self):
        stylesheet = tinycss2.parse_stylesheet(self.css , skip_whitespace = True)
        rules = {}
        prev = None
        for rule in stylesheet:
            selector_string = rule.prelude
            content_string = rule.content

            s_rules = {}
            for content in content_string:
                if type(content) in [tinycss2.ast.WhitespaceToken, tinycss2.ast.LiteralToken]:
                    continue
                if type(content) == tinycss2.ast.IdentToken:
                    if type(prev) == tinycss2.ast.IdentToken:
                        s_rules[prev.value] = content.value
                        prev = None
                        continue
                
                elif type(content) == tinycss2.ast.DimensionToken:
                    if type(prev) == tinycss2.ast.IdentToken:
                        s_rules[prev.value] = content.value
                        prev = None
                        continue

                elif type(content) == tinycss2.ast.StringToken:
                    if type(prev) == tinycss2.ast.IdentToken:
                        s_rules[prev.value] = content.value
                        prev = None
                        continue
                
                elif type(content) == tinycss2.ast.FunctionBlock:
                    if type(prev) == tinycss2.ast.IdentToken:
                        n = []
                        values = content.arguments
                        for value in values:
                            if type(value) in [tinycss2.ast.WhitespaceToken, tinycss2.ast.LiteralToken]:
                                continue
                            n.append(value.value)

                        s_rules[prev.value] = n
                        prev = None
                        continue
                

                prev = content


            rules[selector_string[0].value] = s_rules
        return rules

