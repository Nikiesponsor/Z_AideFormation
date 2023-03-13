@login_required(login_url='connex:log')
def souscrib(request):
    plan=request.GET.get('plan')
    checkplan=PlanAdhesion.objects.filter(type_adhesion=plan).exists()
    if checkplan==False:
        messages.error(request,'erreur')
        return redirect('connex:plan') 
    checkplan=PlanAdhesion.objects.get(type_adhesion=plan)
    prix=int(checkplan.prix)
    print(prix)
    def init_payement(request):
        curl_setopt_array= {

            'CURLOPT_URL':"https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/create",
            'CURLOPT_RETURNTRANSFER' : True,
            'CURLOPT_SSL_VERIFYHOST': False,
            'CURLOPT_SSL_VERIFYPEER' : False,
            'CURLOPT_ENCODING' :"",
            'CURLOPT_MAXREDIRS' : 10,
            'CURLOPT_TIMEOUT' : 0,
            'CURLOPT_FOLLOWLOCATION' : True,
            'CURLOPT_HTTP_VERSION': 'CURL_HTTP_VERSION_1_1',
            'CURLOPT_CUSTOMREQUEST' :"POST",
            'CURLOPT_POSTFIELDS':{
                		"commande": {
						"invoice": {
						  "items": [
							{
							  "name": "Nom de article ou service ou produits",
							  "description": "Description du service ou produits",
							  "quantity": 1,
							  "unit_price": prix,
							  "total_price": prix
							}
						  ],
						  "total_amount": prix,
						  "devise": "XOF",
						  "description": "Descrion de la commande des produits ou services",
						  "customer": "",
						  "customer_firstname":request.user.first_name,
						  "customer_lastname":request.user.last_name,
						  "customer_email":request.user.email
						},
						"store": {
						  "name": "E_commerce",
						  "website_url": "http://127.0.0.1:9000/"
						},
						"actions": {
						  "cancel_url": "http://127.0.0.1:9000/plan",
						  "return_url": "http://127.0.0.1:9000/check",
						  "callback_url": "http://127.0.0.1:9000/check"
						},
						"custom_data": {
						  "transaction_id": "" 
						}
					  }
            },
            "CURLOPT_HTTPHEADER":{
                    "Apikey": settings.LIGIDICASH_API_KEY,
                    'Authorization':  'Bearer '+ settings.LIGIDICASH_TOKEN_KEY,
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
        }
        url=curl_setopt_array['CURLOPT_URL']
        payload=curl_setopt_array['CURLOPT_POSTFIELDS']
        headers=curl_setopt_array['CURLOPT_HTTPHEADER']
        x=requests.post(url, data=json.dumps(payload),headers=curl_setopt_array['CURLOPT_HTTPHEADER'])        
        if x.status_code !=200 :
            return str(x.status_code)
        results =x.json()
        print("le resultats",results)
        return results
    
    initialisation=init_payement(request)
    check=Historique.objects.filter(user=request.user).exists()
    instance=Historique.objects.create(user=request.user,typelan=checkplan,prix=prix,token=initialisation['token'])
    tokens=initialisation['token']
    Adherant.objects.filter(user=instance.user).update(token=initialisation['token'])
    link = initialisation['response_text']
    return  HttpResponseRedirect(link)
    return render(request,'souscrib.html')






def verification(request):
    print("qqqqqqqqqqqqqqqqqqqqqqqq",request.GET.get('token'))
    token=request.GET.get('token')
    # check=Adherant.objects.filter(user=request.user).exists()
    check_historique=Historique.objects.filter(token=token).exists()   
    if check_historique == False:
        messages.error(request,'error')
        return redirect('connex:plan') 
    else:
        # user=Adherant.objects.get(user=request.user)
        # token_code=str(user.token)
        def checkpayement(request):
            curl_setopt_array={
                    'CURLOPT_URL' :"https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/confirm/?invoiceToken="+token,
                    'CURLOPT_RETURNTRANSFER' : True,
                    'CURLOPT_SSL_VERIFYHOST' :False,
                    'CURLOPT_SSL_VERIFYPEER' :False,
                    'CURLOPT_ENCODING' :"",
                    'CURLOPT_MAXREDIRS' :10,
                    'CURLOPT_TIMEOUT' : 30,
                    'CURLOPT_FOLLOWLOCATION' : True,
                    'CURLOPT_HTTP_VERSION': 'CURL_HTTP_VERSION_1_1',
                    'CURLOPT_CUSTOMREQUEST' :"GET",
                    'CURLOPT_HTTPHEADER':{
                            "Apikey": settings.LIGIDICASH_API_KEY,
                            'Authorization':  'Bearer '+ settings.LIGIDICASH_TOKEN_KEY,
                    }          
            }
            url=curl_setopt_array['CURLOPT_URL']
            x=requests.get(url,headers=curl_setopt_array['CURLOPT_HTTPHEADER'])
            if x.status_code !=200:
                return str(x.status_code)
            results= x.json()
            
            return results
        
        initialisation=checkpayement(request)
        if initialisation['status']=='completed':
            print("wwwwwwwwwwwwwwwwwwwwwwwwwwwww",initialisation['token'])
            Historique.objects.filter(token=initialisation['token']).update(payer=True)
            newpayement=Historique.objects.get(token=initialisation['token'])
            instance=PlanAdhesion.objects.get(type_adhesion=newpayement.typelan)
            Adherant.objects.filter(token=initialisation['token']).update(typeplan=instance)
            adher=Adherant.objects.get(token=initialisation['token'])
            Souscription.objects.create(adherant_souscrit=adher,date_expiration=dt.now().date() + timedelta(days=adher.typeplan.dure))
            # link = initialisation['response_text']
            # return  HttpResponseRedirect(link)
            messages.success(request,'payement effectuer avec succes')
            return redirect('connex:plan')
        elif initialisation['status']== 'nocompleted':
            messages.error(request,'vous avez annuller la requete')
            print("annulation  de la demmande ")
            print("reponse text",initialisation['response_text'])
            return redirect('connex:plan')
        elif initialisation['status']=='pending':
            messages.error(request,'payement non valide')
            print("payement non valide")
            print("reponse text",initialisation['response_text']) 
            return redirect('connex:plan')
        link = initialisation['response_text']
        return  HttpResponseRedirect(link)
    return render(request,"verification.html")









# @login_required(login_url='connex:log')
# def souscrib(request):
#     plan=request.GET.get('plan')
#     checkplan=PlanAdhesion.objects.filter(type_adhesion=plan).exists()
#     if checkplan==False:
#         messages.error(request,'erreur')
#         return redirect('connex:plan') 
#     checkplan=PlanAdhesion.objects.get(type_adhesion=plan)
#     prix=int(checkplan.prix)
#     print(prix)
#     PAYDUNYA_ACCESS_TOKENS = {
#     'PAYDUNYA-MASTER-KEY': "test_public_ed6kOIYevVzyoX3BRgf67FjVdMr",
#     'PAYDUNYA-PRIVATE-KEY': "test_private_pW97xCO9qL55YpRAQwFu3tTFn1Z",
#     'PAYDUNYA-TOKEN': "m4eRodEUB6XmQZ2d7TPs"
#     }
#     # Activer le mode 'test'. Le debug est à False par défaut
#     paydunya.debug = True
#     # Configurer les clés d'API
#     paydunya.api_keys = PAYDUNYA_ACCESS_TOKENS

#     # Configuration des informations de votre service/entreprise
#     infos = {
#     'name': "Magasin Chez Sandra", # Seul le nom est requis
#     'tagline': "L'élégance n'a pas de prix",
#     'website_url': "http://127.0.0.1:8000/",
#     'logo_url': "http://127.0.0.1:8000/static/assets/img/logoZ.png"
#     }

#     store = Store(**infos)
#     def initialisation(request):        
#         store = Store(name='Z_aide')
#         items = [
#         InvoiceItem(
#             name="Chaussures Croco",
#             quantity=3,
#             unit_price="10000",
#             total_price="30000",
#             description="Chaussures faites en peau de crocrodile authentique qui chasse la pauvreté"
#         )
#         ]        
#         invoice = paydunya.Invoice(store)
#         invoice.callback_url = "http://www.ma-super-boutique.com/fichier_de_reception_des_données_de_facturation"
#         invoice.add_items(items)
#         successful, response = invoice.create()
#         print("swwwwwwwwwwwwwwwwwwwwwwwwww",response)
#         return response
#     initialisatio=initialisation(request)
#     print("ffffffffffffffffffffffffffff",initialisatio)