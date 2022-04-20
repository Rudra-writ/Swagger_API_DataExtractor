from django.shortcuts import render
from .forms import WikiForm
import pandas as pd
import requests
import json
import glob
import os.path
from django.http import HttpResponse
import tabulate
import mwclient

def first_page(request):
     context ={}
     form = WikiForm(request.POST or None)
     context['form'] = form
     if( 'pull' in request.POST):
        if form.is_valid():
            filters = form.cleaned_data.get("filters")

            url = 'http://requisite.ad.rfa.space/nc/gnc_test_database_dzpx/api/v1/All Requirements?limit=10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

            headers = {'xc-auth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJ1ZHJhd3JpdC5tYWp1bWRhckByZmEuc3BhY2UiLCJmaXJzdG5hbWUiOm51bGwsImxhc3RuYW1lIjpudWxsLCJpZCI6Nywicm9sZXMiOiJ1c2VyIiwiaWF0IjoxNjQ4ODM3MTI1fQ.gC7bcZVMTvwpKTU8nlZrxmfKrapUXhTtrwlVS9EzNi4'}
            r = requests.get(url, headers=headers)

            dict = json.loads(r.text)
            df = pd.json_normalize(dict)
            df2 = pd.DataFrame(columns = ['Req ID','Type'])
            df.reset_index(drop =True, inplace =True)
            df2= df[['Req ID', 'Type']]
            columns = list(df.columns)
            

            df = df[filters]
            if 'Req ID' not in filters:
                df_concat = pd.concat([df, df2['Req ID']], axis = 1)
                print(df_concat)
            else:
                df_concat = df

            if 'Type' not in filters:
                df_concat = pd.concat([df_concat, df2['Type']], axis = 1)
                print(df_concat)
            else:
                df_concat=df_concat
            

            print(filters)
            print(df_concat.head())
            df_concat=df_concat.fillna("none")
            df_concat.set_index( ['Req ID'],drop = True, inplace = True, )
            df_concat['filter_column'] = df_concat.index.str.split("-").str[1].str[-2:]

            if( request.POST.get('department') != '' and request.POST.get('type') != ''):
               df_concat = df_concat[(df_concat.filter_column == request.POST.get('department')) & (df_concat.Type == request.POST.get('type')) ]
            elif ( request.POST.get('department') != ''  and request.POST.get('type') == ''):
                df_concat = df_concat[df_concat.filter_column == request.POST.get('department') ]
            elif ( request.POST.get('department') == ''  and request.POST.get('type') != ''):
                df_concat = df_concat[df_concat.filter_column == request.POST.get('type') ]
            else:
                df_concat = df_concat


            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="GNC_data.xlsx"'                                        
            df_concat.to_excel(response)
  
            return response

        else:
            form = WikiForm

     elif('wiki' in request.POST):

         if form.is_valid():
            filters = form.cleaned_data.get("filters")

            url = 'http://requisite.ad.rfa.space/nc/gnc_test_database_dzpx/api/v1/All Requirements?limit=10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

            headers = {'xc-auth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJ1ZHJhd3JpdC5tYWp1bWRhckByZmEuc3BhY2UiLCJmaXJzdG5hbWUiOm51bGwsImxhc3RuYW1lIjpudWxsLCJpZCI6Nywicm9sZXMiOiJ1c2VyIiwiaWF0IjoxNjQ4ODM3MTI1fQ.gC7bcZVMTvwpKTU8nlZrxmfKrapUXhTtrwlVS9EzNi4'}
            r = requests.get(url, headers=headers)

            dict = json.loads(r.text)
            df = pd.json_normalize(dict)
            df2 = pd.DataFrame(columns = ['Req ID','Type'])
            df.reset_index(drop =True, inplace =True)
            df2= df[['Req ID', 'Type']]
            columns = list(df.columns)
            

            df = df[filters]
            if 'Req ID' not in filters:
                df_concat = pd.concat([df, df2['Req ID']], axis = 1)
                print(df_concat)
            else:
                df_concat = df

            if 'Type' not in filters:
                df_concat = pd.concat([df_concat, df2['Type']], axis = 1)
                print(df_concat)
            else:
                df_concat=df_concat
            

            print(filters)
            print(df_concat.head())
            df_concat=df_concat.fillna("none")
            df_concat = df_concat.replace("-", "none")
            df_concat.set_index( ['Req ID'],drop = True, inplace = True, )
            df_concat['filter_column'] = df_concat.index.str.split("-").str[1].str[-2:]

            if( request.POST.get('department') != '' and request.POST.get('type') != ''):
               df_concat = df_concat[(df_concat.filter_column == request.POST.get('department')) & (df_concat.Type == request.POST.get('type')) ]
            elif ( request.POST.get('department') != ''  and request.POST.get('type') == ''):
                df_concat = df_concat[df_concat.filter_column == request.POST.get('department') ]
            elif ( request.POST.get('department') == ''  and request.POST.get('type') != ''):
                df_concat = df_concat[df_concat.filter_column == request.POST.get('type') ]
            else:
                df_concat = df_concat



            print(df_concat)
          
  
            df_concat.drop(['filter_column'], inplace = True, axis = 1)
            df_concat.reset_index(level = 0, inplace = True)
            table_class = '{| class="wikitable"\n'
            columns = list(df.columns)
            header = ''
            for column in columns:
                header+= '!' + column + '\n'
            row_seperator = '|-\n'
            table = table_class + header 
            for index, rows in df_concat.iterrows():
                col = ''
                col+=row_seperator
                
                for ind, column in rows.iteritems():
                    col+= '|'+column +'\n' if type(column) == str else '|'+ ''.join(column)  +'\n'
                table+=col
                
            table = table + '|}'
            print(table)

            site = mwclient.Site('wiki.ad.rfa.space',scheme='http', path='/', force_login= False)
            site.login('Rudrawrit.majumdar@Rudrawrit', 'ddqr7c5v0heiqdm6uihk3kksrrhiestk')
            Users = ['User:Rudrawrit.majumdar', 'User:Prathamesh.malpathak']
            for user in Users:
                page = site.pages[user]
                text = page.text()
                print(page.exists)
                page.edit(text,'' )
                print (text.encode('utf-8'))
                heading = "== GNC Requirements =="
                
                message = "\n\n{}\n{} --~~~~".format(heading, table)
                page.save(message,summary='testing write api')

             
            file_data = table
            response2 = HttpResponse(file_data, content_type='application/text charset=utf-8')
            response2['Content-Disposition'] = 'attachment; filename="wiki_format.txt"'
    
            return response2
         else:
            form = WikiForm
  
     return render(request, 'first_page.html', context)

 