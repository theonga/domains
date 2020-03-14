from django.shortcuts import render
import whois
# Create your views here.

def WhoisView(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if request.method == 'POST':
        domain = request.POST['domain']
        if domain:
            c = whois.whois(domain)
            resp = "ok"
            d_name = c.domain
            status = c['status']
            updated= c['updated_date']
            exp = c.get('expiration_date')
            registrar = c['registrar']
            dnssec = c['dnssec']
            name = c['name']
            org = c['org']
            state = c['state']
            city = c['city']
            zipcode = c['zipcode']
            country =c['country']
            address =c['address']
            nameservers = c.get('name_servers')
            whois_server = c['whois_server']
            creation_date = c['creation_date']
            emails= c.get('emails')
            return render(
                request,
                'whois/index.html',
                {
                    'ip': ip,
                    'd_name': d_name,
                    'nameservers': nameservers,
                    'exp': exp,
                    'emails': emails,
                    'status': status,
                    'resp': resp,
                    'updated': updated,
                    'registrar': registrar,
                    'dnssec': dnssec,
                    'name': name,
                    'org': org,
                    'address': address,
                    'city': city,
                    'state': state,
                    'zipcode': zipcode,
                    'country': country,
                    'creation_date': creation_date,
                    'whois_server': whois_server,
                }

            )
        else:
            resp = "None"
            return render(request, 'whois/index.html', {'ip': ip, 'resp': resp})
    else:
        resp="none"
        return render(request, 'whois/index.html', {'ip': ip, 'resp': resp})
