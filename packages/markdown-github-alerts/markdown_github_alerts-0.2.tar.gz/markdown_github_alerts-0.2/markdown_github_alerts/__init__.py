from markdown.extensions import Extension
import xml.etree.ElementTree as etree
from markdown.blockprocessors import BlockProcessor
import re
from . import icons

icon_svg = {
    'note': icons.info,
    'tip': icons.light_bulb,
    'important': icons.report,
    'warning': icons.alert,
    'caution': icons.stop
}

class AlertBlockProcessor(BlockProcessor):
    alert_types = ('NOTE', 'TIP', 'IMPORTANT', 'WARNING', 'CAUTION')

    icon_mapping = {
        'note': 'info',
        'tip': 'light-bulb',
        'important': 'report',
        'warning': 'alert',
        'caution': 'stop'
    }

    alert_re_groups = '|'.join(f'({a_type})' for a_type in alert_types)

    ALERT_START = re.compile(
        f'> {{0,1}}\[!(?P<alert_type>{alert_re_groups})] *\n'
    )

    def test(self, parent, block):
        return self.ALERT_START.match(block)

    def run(self, parent, blocks):
        current_block = blocks[0]
        match = self.ALERT_START.match(current_block)
        alert_name = match["alert_type"].lower()
        # Chop off first line containing the alert header
        lines = current_block.split('\n')[1:]

        for idx, line in enumerate(lines):
            # Invalid alert block, do not render
            if ( not re.match('>', line) ):
                return False
            # Chop off leading ">"
            lines[idx] = line[1:]

        alert = etree.SubElement(parent, 'div')
        alert.set('class', f'markdown-alert markdown-alert-{alert_name}')
        header = etree.SubElement(alert, 'p')
        header.set('class', 'markdown-alert-title')
        icon = etree.fromstring(icon_svg[alert_name])

        icon.set(
            'class',
            f'octicon octicon-{self.icon_mapping[alert_name]} mr-2'
        )

        header.append(icon)
        icon.tail = alert_name.capitalize()
        self.parser.parseChunk(alert, '\n'.join(lines))

        # Remove processed block
        blocks.pop(0)

        return True

class MarkdownAlerts(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(
            AlertBlockProcessor(md.parser),
            'alert',
            35
        )

def makeExtension(**kwargs):
    return MarkdownAlerts(**kwargs)
