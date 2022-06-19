import re

from django.shortcuts import render, redirect

from .forms import JurIsikFormSet, OsayhingForm, IsikFormSet, JurIsikForm, IsikForm
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
                                                        registrikood__contains=osayhing_kood).order_by('nimi')

        osayhingud_by_jurisik = None
        osayhingud_by_isik = None

        if if_isik is None:
            osayhingud_by_jurisik = JurIsik.objects \
                .filter(nimi__contains=osanik_nimi, kood__contains=osanik_kood) \
                .values('nimi', 'kood', 'osayhing__id', 'osayhing__nimi', 'osayhing__registrikood') \
                .order_by('osayhing__nimi')
        else:
            if osanik_nimi:
                ees_perenimi_array = osanik_nimi.split(' ')
                if len(ees_perenimi_array) == 1:
                    osayhingud_by_eesnimi = Isik.objects \
                        .filter(eesnimi__contains=ees_perenimi_array[0], isikukood__contains=osanik_kood) \
                        .values('eesnimi', 'perenimi', 'isikukood', 'osayhing__id', 'osayhing__nimi',
                                'osayhing__registrikood')

                    osayhingud_by_perenimi = Isik.objects \
                        .filter(perenimi__contains=ees_perenimi_array[0], isikukood__contains=osanik_kood) \
                        .values('eesnimi', 'perenimi', 'isikukood', 'osayhing__id', 'osayhing__nimi',
                                'osayhing__registrikood')

                    osayhingud_by_isik = osayhingud_by_eesnimi.union(osayhingud_by_perenimi).order_by('osayhing__nimi')
                else:
                    osayhingud_by_isik = Isik.objects \
                        .filter(eesnimi__contains=ees_perenimi_array[0], perenimi__contains=ees_perenimi_array[1]) \
                        .values('eesnimi', 'perenimi', 'isikukood', 'osayhing__id', 'osayhing__nimi',
                                'osayhing__registrikood') \
                        .order_by('osayhing__nimi')

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


def detailsview(request, oy_id):

    osayhing = Osayhing.objects.get(id=oy_id)
    formatted_asutamiskuup = osayhing.asutamiskuup.strftime('%d.%m.%Y')
    osanikud_jurisik = JurIsik.objects.filter(osayhing__id=oy_id)
    osanikud_isik = Isik.objects.filter(osayhing__id=oy_id)


    return render(request, 'register/details.html', {
        'osayhing': osayhing,
        'osanikud_jurisik': osanikud_jurisik,
        'osanikud_isik': osanikud_isik,
        'formatted_asutamiskuup': formatted_asutamiskuup,
    })


def addview(request):
    kapital_error = None
    osade_sum = 0

    if request.method == 'GET':
        osayhing_form = OsayhingForm(request.GET or None)
        jur_isik_formset = JurIsikFormSet(queryset=JurIsik.objects.none())
        isik_formset = IsikFormSet(queryset=JurIsik.objects.none())

        return render(request, 'register/add.html', {
            'osayhing_form': osayhing_form,
            'jur_isik_formset': jur_isik_formset,
            'isik_formset': isik_formset
        })
    if request.method == 'POST':
        osayhing_form = OsayhingForm(request.POST)
        jur_isik_formset = JurIsikFormSet(request.POST)
        isik_formset = IsikFormSet(request.POST)

        if osayhing_form.is_valid() and jur_isik_formset.is_valid() and isik_formset.is_valid():
            kogukapital = osayhing_form.cleaned_data.get('kogukapital')

            for form in jur_isik_formset:
                if form.cleaned_data != {}:
                    osade_sum += form.cleaned_data.get('j_osaniku_osa')

            for form in isik_formset:
                if form.cleaned_data != {}:
                    osade_sum += form.cleaned_data.get('f_osaniku_osa')

            if kogukapital == osade_sum:
                osayhing = osayhing_form.save()
                for form in jur_isik_formset:
                    if form.cleaned_data != {}:
                        jur_isik = form.save(commit=False)
                        jur_isik.osayhing = osayhing
                        jur_isik.asutaja = True
                        jur_isik.save()
                for form in isik_formset:
                    if form.cleaned_data != {}:
                        isik = form.save(commit=False)
                        isik.osayhing = osayhing
                        isik.asutaja = True
                        isik.save()

                return redirect('Osaühingu andmete vaade', osayhing.id)
            else:
                kapital_error = 'Kogukaiptali suurus on erinev osaniku osade summadega'

        return render(request, 'register/add.html', {
            'kapital_error': kapital_error,
            'osayhing_form': osayhing_form,
            'jur_isik_formset': jur_isik_formset,
            'isik_formset': isik_formset,
        })


def editview(request, oy_id):
    osayhing = Osayhing.objects.get(id=oy_id)
    formatted_asutamiskuup = osayhing.asutamiskuup.strftime('%d.%m.%Y')
    osanikud_jurisik = JurIsik.objects.filter(osayhing__id=oy_id)
    osanikud_isik = Isik.objects.filter(osayhing__id=oy_id)

    if request.method == 'GET':
        jur_isik_form = JurIsikForm(request.GET or None)
        isik_form = IsikForm(request.GET or None)

        return render(request, 'register/edit.html', {
            'osayhing': osayhing,
            'osanikud_jurisik': osanikud_jurisik,
            'osanikud_isik': osanikud_isik,
            'formatted_asutamiskuup': formatted_asutamiskuup,
            'jur_isik_form': jur_isik_form,
            'isik_form': isik_form,
        })

    if request.method == 'POST':
        j_osanik_string = request.POST.get('j-osanik')
        if j_osanik_string is not None:
            j_osanik_kood = re.findall("\d+", j_osanik_string)[0]
            j_osanik = JurIsik.objects.get(kood=j_osanik_kood)

            old_j_osaniku_osa = j_osanik.j_osaniku_osa
            try:
                new_j_osaniku_osa = int(request.POST['j-osaniku-osa'])
                kapital = osayhing.kogukapital + new_j_osaniku_osa - old_j_osaniku_osa
                if kapital >= 2500:
                    j_osanik.j_osaniku_osa = new_j_osaniku_osa
                    j_osanik.save()
                    osayhing.kogukapital = kapital
                    osayhing.save()
                    return redirect('Osaühingu andmete vaade', osayhing.id)
            except ValueError:
                print("Uue osaniku osa value not int")

        f_osanik_string = request.POST.get('f-osanik')
        if f_osanik_string is not None:
            f_osanik_isikukood = re.findall("\d+", f_osanik_string)[0]
            f_osanik = Isik.objects.get(isikukood=f_osanik_isikukood)

            old_f_osaniku_osa = f_osanik.f_osaniku_osa
            try:
                new_f_osaniku_osa = int(request.POST['f-osaniku-osa'])
                kapital = osayhing.kogukapital + new_f_osaniku_osa - old_f_osaniku_osa
                if kapital >= 2500:
                    f_osanik.f_osaniku_osa = new_f_osaniku_osa
                    f_osanik.save()
                    osayhing.kogukapital = kapital
                    osayhing.save()
                    return redirect('Osaühingu andmete vaade', osayhing.id)
            except ValueError:
                print("Uue osaniku osa value not int")

        jur_isik_form = JurIsikForm(request.POST)
        isik_form = IsikForm(request.POST)
        if jur_isik_form.is_valid():
            jur_isik = jur_isik_form.save(commit=False)
            osayhing.kogukapital += jur_isik.j_osaniku_osa
            osayhing.save()

            jur_isik.osayhing = osayhing
            jur_isik.asutaja = False
            jur_isik.save()

        if isik_form.is_valid():
            isik = isik_form.save(commit=False)
            osayhing.kogukapital += isik.f_osaniku_osa
            osayhing.save()

            isik.osayhing = osayhing
            isik.asutaja = False
            isik.save()

            return redirect('Osaühingu andmete vaade', osayhing.id)



    return render(request, 'register/edit.html', {
        'osayhing': osayhing,
        'osanikud_jurisik': osanikud_jurisik,
        'osanikud_isik': osanikud_isik,
        'formatted_asutamiskuup': formatted_asutamiskuup,
    })
