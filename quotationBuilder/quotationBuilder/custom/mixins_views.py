from django.utils import timezone
from quotationBuilder import __version__


class StatusFieldMixin():
    '''
    Adds status-fields to the API responses
    '''

    response_desc = ''
    skip_status = False
    fields = '__all__'

    def add_status_info(self, response):
        # check if status is ok
        if response.status_code >= 200 and response.status_code < 300:
            ok = True
        else:
            ok = False

        # find out length of response data
        count = None
        if response is not None:
            if response.data is not None:
                count = len(response.data)

        if not self.skip_status:
            response.data = {
                "besVersion": __version__,
                "ok": ok,
                "message": self.response_desc,
                "status": response.status_code,
                "statusText": response.status_text,
                "timestamp": timezone.now(),
                "count": count,
                "data": response.data,
            }
        return response

    def dispatch(self, request, *args, **kwargs):
        response = super(StatusFieldMixin, self).dispatch(
            request, *args, **kwargs)
        return self.add_status_info(response)
