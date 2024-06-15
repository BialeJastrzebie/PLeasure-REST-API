from django.core.management import call_command


def clear_expired_coupons():
    call_command('remove_expired_coupons')

