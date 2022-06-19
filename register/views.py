import re

from django.shortcuts import render, redirect

from .forms import JurIsikFormSet, OsayhingForm, IsikFormSet, JurIsikForm, IsikForm
from .models import Osayhing, Isik, JurIsik


# Register app views

# Avaleht
def indexview(request):
    """
    It takes the user input from the form, and then queries the database for the relevant information

    param request: The request object is an HttpRequest object. It contains metadata about the request,
    including the HTTP method
    :return: a render object.
    """

    # Checking if the request method is POST when user sends search query
    if request.method == 'POST':
        osayhing_nimi = request.POST['osayhing-nimi'].strip()
        osayhing_kood = request.POST['osayhing-kood'].strip()
        osanik_nimi = request.POST['osanik-nimi'].strip()
        osanik_kood = request.POST['osanik-kood'].strip()
        if_isik = request.POST.get('if-isik')   # checkbox data

        # query the database for saved company entities by company name and/or register code
        osayhingud_by_oy_data = Osayhing.objects.filter(nimi__contains=osayhing_nimi,
                                                        registrikood__contains=osayhing_kood).order_by('nimi')

        osayhingud_by_jurisik = None
        osayhingud_by_isik = None

        # if shareholder is not a physical person, query by company by name and/or code of juridical person
        if if_isik is None:
            osayhingud_by_jurisik = JurIsik.objects \
                .filter(nimi__contains=osanik_nimi, kood__contains=osanik_kood) \
                .values('nimi', 'kood', 'osayhing__id', 'osayhing__nimi', 'osayhing__registrikood') \
                .order_by('osayhing__nimi')
        else:
            # if shareholder is physical person, check if query by name and family name or by both and query by names
            # and personal code
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
        context = {
            'osayhing_nimi': osayhing_nimi,
            'osayhing_kood': osayhing_kood,
            'osanik_nimi': osanik_nimi,
            'osanik_kood': osanik_kood,
            'osayhingud_by_oy_data': osayhingud_by_oy_data,
            'osayhingud_by_jurisik': osayhingud_by_jurisik,
            'osayhingud_by_isik': osayhingud_by_isik
        }
    else:
        context = {}

    return render(request, 'register/index.html', context)


# Osayhingu andmete vaade
def detailsview(request, oy_id):
    """
    It takes the id of an Osayhing object, gets the object from the database, formats the date, gets the JurIsik and
    Isik objects that are related to the Osayhing object, and then passes all of that to the template

    param request: The request object is an HttpRequest object. It contains metadata about the request
    param oy_id: the id of the Osayhing object
    :return: a render of the details.html template with the context.
    """
    osayhing = Osayhing.objects.get(id=oy_id)
    formatted_asutamiskuup = osayhing.asutamiskuup.strftime('%d.%m.%Y')
    osanikud_jurisik = JurIsik.objects.filter(osayhing__id=oy_id)
    osanikud_isik = Isik.objects.filter(osayhing__id=oy_id)

    context = {
        'osayhing': osayhing,
        'osanikud_jurisik': osanikud_jurisik,
        'osanikud_isik': osanikud_isik,
        'formatted_asutamiskuup': formatted_asutamiskuup,
    }
    return render(request, 'register/details.html', context)


def addview(request):
    """
    If the request method is GET, then create an empty form and render it.
    If the request method is POST, then create a form instance and populate it with data from the request:

    Examples:
    form = NameForm(request.POST)

    Check if the form is valid:

    if form.is_valid():
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        return HttpResponseRedirect('/thanks/')

    If the form is valid, Django will normalize the data and save it to a dictionary accessible via the cleaned_data
    attribute of the Form class

    If all checks passed, Django will save generated from Form data entities to database and redirect to
    `Osayhingu andmete vaade` page

    param request: The request object is an HttpRequest object. It contains metadata about the request, such as the HTTP
    method
    :return: a render of the add.html template with the context.
    """

    context = {}

    kapital_error = None
    osade_sum = 0   # sum of shareholders capitals

    if request.method == 'GET':
        osayhing_form = OsayhingForm(request.GET or None)
        jur_isik_formset = JurIsikFormSet(queryset=JurIsik.objects.none())
        isik_formset = IsikFormSet(queryset=JurIsik.objects.none())

        context = {
            'osayhing_form': osayhing_form,
            'jur_isik_formset': jur_isik_formset,
            'isik_formset': isik_formset
        }

    if request.method == 'POST':
        osayhing_form = OsayhingForm(request.POST)
        jur_isik_formset = JurIsikFormSet(request.POST)
        isik_formset = IsikFormSet(request.POST)

        # Forms validity check
        if osayhing_form.is_valid() and jur_isik_formset.is_valid() and isik_formset.is_valid():
            # Gets company total capital sum from form cleaned data
            kogukapital = osayhing_form.cleaned_data.get('kogukapital')

            # Adds juridical persons (shareholders) capitals to sum of shareholders capitals
            for form in jur_isik_formset:
                if form.cleaned_data != {}:
                    osade_sum += form.cleaned_data.get('j_osaniku_osa')

            # Adds physical persons (shareholders) capitals to sum of shareholders capitals
            for form in isik_formset:
                if form.cleaned_data != {}:
                    osade_sum += form.cleaned_data.get('f_osaniku_osa')

            # If sum matches with company capital, then save and redirect
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

        context = {
            'kapital_error': kapital_error,
            'osayhing_form': osayhing_form,
            'jur_isik_formset': jur_isik_formset,
            'isik_formset': isik_formset,
        }

    return render(request, 'register/add.html', context)


# Osayhingu osakapitali suurendamise vorm
def editview(request, oy_id):
    """
    If request method GET, it takes an Osayhing object, gets all the JurIsik and Isik objects that are related to it,
    and then renders a template with all the data

    If request method POST, then update fetched objects with data from the request

    param request: The request object is the first parameter to the view function. It contains the HTTP request sent by
    the user
    param oy_id: the id of the Osayhing object
    :return: a render of the edit.html template.
    """

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
        # If updating juridical person`s capital, receiving string of object required for update.
        j_osanik_string = request.POST.get('j-osanik')
        if j_osanik_string is not None:
            j_osanik_kood = re.findall("\d+", j_osanik_string)[0]
            j_osanik = JurIsik.objects.get(kood=j_osanik_kood)

            # Storing old shareholder capital amount for recalculation of company total capital
            old_j_osaniku_osa = j_osanik.j_osaniku_osa
            # Trying to get new shareholder capital string from request and convert it to Integer, if it is convertable,
            # then recalculate capitals and update company and shareholder entities.
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

        # The similar procedure for physical person object, if updating physical person`s capital
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

        # Procedure for saving juridical or physical person if new shareholders added.
        jur_isik_form = JurIsikForm(request.POST)
        isik_form = IsikForm(request.POST)
        if jur_isik_form.is_valid():
            jur_isik = jur_isik_form.save(commit=False)
            osayhing.kogukapital += jur_isik.j_osaniku_osa
            osayhing.save()

            jur_isik.osayhing = osayhing
            jur_isik.asutaja = False
            jur_isik.save()

            return redirect('Osaühingu andmete vaade', osayhing.id)

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
