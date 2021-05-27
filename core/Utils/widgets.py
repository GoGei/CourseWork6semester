from django.utils.safestring import mark_safe
from sdh.table import widgets as table_widgets


class BooleanWidget(table_widgets.BaseWidget):
    def html_cell(self, row_index, row, **kwargs):
        value = self.get_value(row)
        if value is None:
            class_icon = 'none fa fa-exclamation-triangle text-warning'
        elif value:
            class_icon = 'true fa fa-check-circle text-navy'
        else:
            class_icon = 'false fa fa-minus-circle text-danger'

        return mark_safe('<i class="%s" aria-hidden="true"></i>' % class_icon)
