import datetime
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from voucher.models import WorkLog
from voucher.utils import get_first_valid_work_log_date


def valid_date_worked(date):
    if date < get_first_valid_work_log_date():
        raise serializers.ValidationError(
            detail=_("Date %(date)s is too far in the past")
            % {"date": date.isoformat()}
        )
    if date > datetime.date.today():
        raise serializers.ValidationError(
            detail=_("Date %(date)s is in the future") % {"date": date.isoformat()}
        )


class ValidVouchers(object):
    serializer_field = None

    def __call__(self, value):
        if value > 0:
            return

        perm = "%s.delete_%s" % (WorkLog._meta.app_label, WorkLog._meta.model_name)
        if self.serializer_field.parent.context.request.user.has_perm(perm):
            return

        raise serializers.ValidationError(detail=_("Vouchers must be positive"))

    def set_context(self, serializer_field):
        self.serializer_field = serializer_field
