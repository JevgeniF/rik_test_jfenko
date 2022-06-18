from django.shortcuts import render

from .models import Osayhing, Isik, JurIsik


# Create your views here.

def indexview(request):
    if request.method == 'POST':
        osayhing_nimi = request.POST['osayhing-nimi'].strip()
        osayhing_kood = request.POST['osayhing-kood'].strip()
        osanik_nimi = request.POST['osanik-nimi'].strip()
        osanik_kood = request.POST['osanik-kood'].strip()
        if_isik = request.POST.get('if-isik')

        osayhingud_by_oy_data = Osayhing.objects.filter(nimi__contains=osayhing_nimi,
                                                        registrikood__contains=osayhing_kood)

        osayhingud_by_jurisik = None
        osayhingud_by_isik = None

        if if_isik is None:
            osayhingud_by_jurisik = JurIsik.objects.filter(nimi__contains=osanik_nimi,
                                                           kood__contains=osanik_kood).values('nimi', 'kood',
                                                                                              'osayhing__nimi',
                                                                                              'osayhing__registrikood')
        else:
            if osanik_nimi:
                ees_perenimi_array = osanik_nimi.split(' ')
                if len(ees_perenimi_array) == 1:
                    osayhingud_by_eesnimi = Isik.objects.filter(eesnimi__contains=ees_perenimi_array[0],
                                                                isikukood__contains=osanik_kood).values('eesnimi',
                                                                                                        'perenimi',
                                                                                                        'isikukood',
                                                                                                        'osayhing__nimi',
                                                                                                        'osayhing__registrikood')
                    osayhingud_by_perenimi = Isik.objects.filter(perenimi__contains=ees_perenimi_array[0],
                                                                 isikukood__contains=osanik_kood).values('eesnimi',
                                                                                                         'perenimi',
                                                                                                         'isikukood',
                                                                                                         'osayhing__nimi',
                                                                                                         'osayhing__registrikood')
                    osayhingud_by_isik = osayhingud_by_eesnimi.union(osayhingud_by_perenimi)
                else:
                    osayhingud_by_isik = Isik.objects.filter(eesnimi__contains=ees_perenimi_array[0],
                                                             perenimi__contains=ees_perenimi_array[1]).values('eesnimi',
                                                                                                              'perenimi',
                                                                                                              'isikukood',
                                                                                                              'osayhing__nimi',
                                                                                                              'osayhing__registrikood')

        return render(request, 'register/index.html', {
            'osayhing_nimi': osayhing_nimi,
            'osayhing_kood': osayhing_kood,
            'osanik_nimi': osanik_nimi,
            'osanik_kood': osanik_kood,
            'osayhingud_by_oy_data': osayhingud_by_oy_data,
            'osayhingud_by_jurisik': osayhingud_by_jurisik,
            'osayhingud_by_isik': osayhingud_by_isik
        })
    else:
        return render(request, 'register/index.html', {})


def detailsview(request):
    return render(request, 'register/details.html')


def addview(request):
    return render(request, 'register/add.html')


def editview(request):
    return render(request, 'register/edit.html')
