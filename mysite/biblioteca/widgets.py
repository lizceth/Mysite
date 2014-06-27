# -*- coding: utf-8 -*-

from django.utils.encoding import force_unicode
from mysite import settings
from django import forms
import datetime, time
from django.utils.safestring import mark_safe
from django.utils import formats


# DATETIMEWIDGET
calbtn = u"""<img src="%scustom/calendario_admin/imagenbutton/calbutton.gif" alt="calendar" id="%s_btn" style="cursor: pointer;" title="Select a date " onmouseover="this.style.background='#ffffff';" onmouseout="this.style.background=''" />
<script type="text/javascript">
   var cal = Calendar.setup ({
            inputField: "%s",
            dateFormat: "%s",
            trigger: "%s_btn",
            bottomBar: false,
            onSelect: function() {
                  this.hide();
                          }
                  });
</script>"""

class DateTimeWidget(forms.widgets.TextInput):
    dformat = '%d/%m/%Y'
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '': 
            try:
                final_attrs['value'] = \
                                   force_unicode(value.strftime(self.dformat))
            except:
                final_attrs['value'] = \
                                   force_unicode(value)
        if not final_attrs.has_key('id'):
            final_attrs['id'] = u'%s_id' % (name)
        id = final_attrs['id']
        
        jsdformat = self.dformat
        cal = calbtn % (settings.STATIC_URL, id, id, jsdformat, id)
        a = u'<input%s />%s' % (forms.util.flatatt(final_attrs), cal)
        return mark_safe(a)

    def value_from_datadict(self, data, files, name):
        #dtf = forms.fields.DEFAULT_DATETIME_INPUT_FORMATS
        dtf = formats.get_format('DATETIME_INPUT_FORMATS')
        empty_values = forms.fields.EMPTY_VALUES

        value = data.get(name, None)
        if value in empty_values:
            return None
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)
        for format in dtf:
            try:
                return datetime.datetime(*time.strptime(value, format)[:6])
            except ValueError:
                continue
        return None