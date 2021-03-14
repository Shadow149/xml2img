# XML2img

Simple module to create images from xml and css

Built with:
- Pillow
- parsel
- tinycss2

## XML and CSS syntax

### XML

- Image : `<Image src='SOURCE'>`
- Title : `<Title text='TEXT'>`
- Label : `<Label text='TEXT'>`
- Section : `<Section>` - Defines a section to apply CSS to (margins etc.)
- Block : `<Block>` - Defines a solid block of colour

### CSS

Most values in pixels only (px)

- margin-top
- margin-bottom
- margin-left
- margin-right
- color (rgb only)
- width
- height
- font-family (dir location)
- font-size
- display (inline or else)

## Example

Inherit `XMLImage` and initialise parameters
```python
class Foo (XMLImage):
    def __init__(self, width, height, xml_path, css_path, background_colour, constants):
        super().__init__(width, height, xml_path, css_path, background_colour, constants)
```

Initialise variables using the `set_variable` method, to use within the XML via double curly braces
```python
    def initialise_variables(self):
        self.set_variable("bar", "this is some text")
        pass
```

Python
```python
from xml2img.XMLImage import XMLImage
from xml2img.Constants import Constants

class Foo (XMLImage):
    def __init__(self, width, height, xml_path, css_path, background_colour, constants, debug):
        super().__init__(width, height, xml_path, css_path, background_colour, constants, debug)

    def initialise_variables(self):
        self.set_variable("bar", "this is some text")
        pass

if __name__ == "__main__":
    consts = Constants(text_colour=(0,0,0))
    image = Foo(500,700,'layouts/image.xml','styles/style.css', (255, 255, 255), consts)
    image.initialise_variables()
    image.create()
```

XML
```xml
<root>
    <Section>
        <Title text="This is a title"/>
        <Label id="margin" text="This is some text"/>
        
        <Section id="inline">
            <Label text="This is some more text, next to an image"/>
            <Image src="./dir/to/img.png">
        </Section>
            
    </Section>
</root>
```

CSS
```css
#margin{
    margin-left: 25px;
}

#inline {
    display: inline;
}
```