from django.conf import settings

from clients.models import Client
from django.db.models import Prefetch, Sum
from django.core.cache import cache
from rest_framework.viewsets import ReadOnlyModelViewSet

from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client',
                 queryset=Client.objects.all().select_related('user').only('company_name',
                                                                           'user__email')
                 )
    )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        response_data = {'result': response.data}
        cache_total_price = cache.get(settings.PRICE_CACHE_NAME)
        if cache_total_price:
            total_price = cache_total_price
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60 * 60)
        response_data['total_amount'] = total_price
        response.data = response_data

        return response
