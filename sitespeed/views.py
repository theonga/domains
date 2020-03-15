from django.shortcuts import render
import urllib
import urllib
from django.conf import settings
# Create your views here.
def SiteSpeedView(request):
    if request.method == 'POST':
        url = request.POST['domain']
        if url:
            device_type = 'mobile'
            escaped_url = urllib.parse.quote(url)
            contents = urllib.request.urlopen(
                'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://{}&strategy={}'
                .format(escaped_url, device_type)
            ).read().decode('UTF-8')
            return render(request, 'sitespeed/index.html', {'response': contents})
    else:
        return render(request, 'sitespeed/index.html')
