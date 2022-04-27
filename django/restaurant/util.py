def generate_response_preorder_pdf(preorder):
    from django.http import HttpResponse
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'attachment; filename="preorder.pdf"'
    # generate_pdf(preorder=preorder, response=response)
    pdftext = generate_pdf(preorder=preorder)
    response.write(pdftext)
    return response


# def generate_pdf(preorder, response):
def generate_pdf(preorder):
    import os
    from django.conf import settings as django_settings

    if "nt" in os.name:
        GTK_FOLDER = r'C:\Program Files\GTK3-Runtime Win64\bin'
        os.environ['PATH'] = GTK_FOLDER + \
            os.pathsep + os.environ.get('PATH', '')
    from django.template.loader import render_to_string
    # The following comment needs uncommented only for testing on win10
    # os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")
    from weasyprint import HTML
    from restaurant.models import MenueInRestaraunt
    orders = []
    for menuinpreorder in preorder.menues.all():
        menue_in_restaraunt = MenueInRestaraunt.objects.filter(menue=menuinpreorder.menue,
                                                               restaraunt=menuinpreorder.preorder.restaraunt).first()
        orders.append({"dish": menuinpreorder.menue.dish,
                      "price":  menue_in_restaraunt.price})
    html_string = render_to_string(
        'report/preorder.html', {
            'orders': orders, 
            'total_price': preorder.price, 
            'restaraunt': preorder.restaraunt
        })
    html = HTML(string=html_string)
    result = html.write_pdf()
    # preorders_root = os.path.join(django_settings.MEDIA_URL, 'preorders')

    print('\n'+'-'*40 +'\n', 'TYPE OF RESULT: ', type(result), '\n'+'-'*40, sep="")

    return result