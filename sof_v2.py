import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import base64


TOKEN = '3e51c1df3a878da1833d6f83a5315bb'
base_url = "https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/v3.0.1"
headers={'Authorization' : str('Bearer ' + TOKEN)}
anos = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
#Anos desejados na consulta; é possível consultar informações a partir de 2003


access_token = 'c3877281dc47f368ebd0f4a9fa9df1a6'

url = 'https://gatewayapi.prodam.sp.gov.br:443/token'
#url = 'https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/v3.0.1/despesas'


import base64
import requests
import json


consumer_key = 'OaX5gyq8SjbnR_UsDNWjHZYrE3Ea'
consumer_secret = 'oN11nczwTCrE5yuWVmdUyfllXswa'
consumer_key_secret = consumer_key+":"+consumer_secret
consumer_key_secret_enc = base64.b64encode(consumer_key_secret.encode()).decode()

# Your decoded key will be something like:
#zzRjettzNUJXbFRqWENuuGszWWllX1iiR0VJYTpRelBLZkp5a2l2V0xmSGtmZ1NkWExWzzhDaWdh


headersAuth = {
    'Authorization': 'Basic '+ str(consumer_key_secret_enc),
}

data = {
  'grant_type': 'password',
}


response = requests.post(url, headers=headersAuth, data=data, verify=True)
j = response.json()

df_lista = []


for ano in anos:
    """consulta todos os anos da lista acima"""
    
    periodo = ano
    
    headersAPI = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+j['access_token'],
    }

    ### Usage of parameters defined in your API
    params = (
        ('anoEmpenho', ano),
        ('mesEmpenho', '12'),
    )


    #url_orcado = '{base_url}/consultarDespesas?anoDotacao={ano}&mesDotacao=12&codOrgao=16'.format(base_url=base_url, ano=ano)
    #print (url_orcado)
    #request_orcado  = requests.post(url_orcado, headers=headersAuth, data=data, verify=True)
    #print (request_orcado.text)
    
    print('Aguarde, gerando lista de DESPESAS do mes 12/'+str(periodo)+' ...')
    response_despesas = requests.get('https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/v3.0.1/despesas?anoDotacao='+str(ano)+'&mesDotacao=12', headers=headersAPI, params=params, verify=True)
    api_response = response_despesas.json()
    #print (api_response)

    arr_despesas = api_response['lstDespesas']
    for key,value in arr_despesas.items():
        print ('\t', str(key)+': '+str(value))

    #for item in api_response['lstDespesas']:
    #    print(item)

    """  
    import pandas as pds
    df = pds.DataFrame(api_response)
    # Write the DataFrame to an excel file
    df.to_excel("Expense.xlsx")
    """

    with open(r'dados_prodam\prod_despesas_'+str(periodo)+'.12.json', 'w', encoding='utf-8') as f:
        json.dump(api_response, f, ensure_ascii=False, indent=4)
    


    print('Aguarde, gerando lista de UNIDADES do mes 12/'+str(periodo)+' ...')
    response_unidades = requests.get('https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/v3.0.1/unidades?codOrgao=16&anoExercicio='+str(ano), headers=headersAPI, params=params, verify=True)
    api_response = response_unidades.json()
    #print (api_response)
   
    """
    arr_unidades = api_response['lstUnidades']
    for key,value in arr_unidades.items():
        print ('\t', str(key)+': '+str(value))
    """
    
    with open(r'dados_prodam\prod_unidades_'+str(periodo)+'.12.json', 'w', encoding='utf-8') as f:
        json.dump(api_response, f, ensure_ascii=False, indent=4)
        
    print('Aguarde, gerando lista de ORGÃOS do mes 12/'+str(periodo)+' ...')
    response_orgaos = requests.get('https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/v3.0.1/orgaos?anoExercicio='+str(ano), headers=headersAPI, params=params, verify=True)
    api_response = response_orgaos.json()
    #print (api_response)
    """
    arr_orgaos = api_response['lstOrgaos']
    for key,value in arr_orgaos.items():
        print ('\t', str(key)+': '+str(value))
    """

    

    
    with open(r'dados_prodam\prod_orgaos_'+str(periodo)+'.12.json', 'w', encoding='utf-8') as f:
        json.dump(api_response, f, ensure_ascii=False, indent=4)
        
    

print('Operação concluida...')