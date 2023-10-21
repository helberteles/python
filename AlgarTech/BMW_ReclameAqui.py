import pandas as pd
import os, re
import numpy as np
from datetime import date, datetime, timedelta


class FuncoesGlobais:

    def convSTRpDATA_SOLICITACAO(string):
        try:
            retorno = format(datetime.strptime(string[:10].strip(), '%Y-%m-%d').date(),'%d/%m/%Y')
        except:
            retorno = None
        return retorno


    def convDT_SEMANA(string):
        semana = ['2ª seg','3ª ter','4ª qua','5ª qui','6ª sex','7ª sab','1ª dom']
        if(string == None):
            retorno = None
        else:
            retorno = semana[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]
        return retorno


    def convDT_ANO(string):
        if(string == None):
            retorno = None
        else:
            retorno = string[:4]
        return retorno


    def convDT_MES(string):
        if(string == None):
            retorno = None
        else:
            retorno = string[5:7]
        return retorno


class ListasAuxiliares:

    def listAUX():
        meses_ano = [["01","01-JANEIRO"],["02","02-FEVEREIRO"],["03","03-MARÇO"],["04","04-ABRIL"],["05","05-MAIO"],["06","06-JUNHO"],["07","07-JULHO"],["08","08-AGOSTO"],["09","09-SETEMBRO"],["10","10-OUTUBRO"],["11","11-NOVEMBRO"],["12","12-DEZEMBRO"]]
        vMESES = pd.DataFrame(data=meses_ano,columns=['num_mes','nome_mes'])
        return vMESES


class PastasGenericas:

    ptRA = r'//acsfs/DEPTOS/CPC/4 - MIS/2 - Cliente/36 - ReclameAqui/01 - BMW/RA'
    ptDESATIVADOS = '//acsfs/DEPTOS/CPC/4 - MIS/2 - Cliente/36 - ReclameAqui/01 - BMW/RA Desativado/'

class ExcelRA_MODERACOES:


    def ExcelRA():

        p = PastasGenericas

        lPASTA = [1]
        RA_CONSOLIDADO = pd.DataFrame()

        for i in lPASTA:

            vLISTA = [os.path.join(p.ptRA, nome) for nome in os.listdir(p.ptRA)]
            vlist_arquivo = [arq for arq in vLISTA if os.path.isfile(arq)]
            vlist_xls = [arq for arq in vlist_arquivo if arq.lower().endswith(".xlsx")]

            RA_ATIVADOS = pd.DataFrame()
            for arq in vlist_xls:
                arquivo_csv = pd.read_excel(arq, encoding='latin_1', skiprows=3) #header=None, skiprows = elimina linhas do df
                arquivo_csv['nome_arquivo']= str(re.findall(r'RA\\.*',arq)).replace(r'RA\\','').replace("['",'').replace("']",'')
                RA_ATIVADOS = RA_ATIVADOS.append(arquivo_csv)

            RA_ATIVADOS = RA_ATIVADOS[['Atribuido Para','Id HugMe','Moderação data de solicitação','Moderação motivo','Moderação status',
                                        'Nível I - Empresa',
                                        'Nível II - Motivos',
                                        'Nível III - Acessórios / Lifestyle / Riders','Nível III - Atendimento','Nível III - Financeiro','Nível III - Institucional',
                                        'Nível III - Peças','Nível III - Processo de Compra','Nível III - Produto','Nível III - Recall','Nível III - Serviços','Nível III - Tecnologia',
                                        'Nível IV - Modelo Veículo BMW Brasil','Nível IV - Modelo Veículo BMW Motorrad','Nível IV - Modelo Veículo MINI',
                                        'Avaliações desconsideradas RA',
                                        'nome_arquivo']]

            RA_ATIVADOS = RA_ATIVADOS.dropna(subset=['Moderação status'])
            RA_ATIVADOS['nome_base'] = 'Ativados'
            RA_ATIVADOS['registros'] = 1
            RA_ATIVADOS.index = pd.RangeIndex(len(RA_ATIVADOS.index))
            RA_CONSOLIDADO = RA_CONSOLIDADO.append(RA_ATIVADOS)

        #------------------------------------------------------------------------------------------

            vLISTA = [os.path.join(p.ptDESATIVADOS, nome) for nome in os.listdir(p.ptDESATIVADOS)]
            vlist_arquivo = [arq for arq in vLISTA if os.path.isfile(arq)]
            vlist_xls = [arq for arq in vlist_arquivo if arq.lower().endswith(".xlsx")]

            RA_DESATIVADOS = pd.DataFrame()
            for arq in vlist_xls:
                arquivo_csv = pd.read_excel(arq, encoding='latin_1', skiprows=3) #header=None, skiprows = elimina linhas do df
                arquivo_csv['nome_arquivo']= str(re.findall(r'RA Desativado/.*',arq)).replace(r'RA Desativado/','').replace("['",'').replace("']",'')
                RA_DESATIVADOS = RA_DESATIVADOS.append(arquivo_csv)


            RA_DESATIVADOS = RA_DESATIVADOS[['Atribuido Para','Id HugMe','Moderação data de solicitação','Moderação motivo','Moderação status',
                                        'Nível I - Empresa',
                                        'Nível II - Motivos',
                                        'Nível III - Acessórios / Lifestyle / Riders','Nível III - Atendimento','Nível III - Financeiro','Nível III - Institucional',
                                        'Nível III - Peças','Nível III - Processo de Compra','Nível III - Produto','Nível III - Recall','Nível III - Serviços','Nível III - Tecnologia',
                                        'Nível IV - Modelo Veículo BMW Brasil','Nível IV - Modelo Veículo BMW Motorrad','Nível IV - Modelo Veículo MINI',
                                        'Avaliações desconsideradas RA',
                                        'nome_arquivo']]

            RA_DESATIVADOS = RA_DESATIVADOS.dropna(subset=['Moderação status'])
            RA_DESATIVADOS['nome_base'] = 'Desativados'
            RA_DESATIVADOS['registros'] = 1
            RA_DESATIVADOS.index = pd.RangeIndex(len(RA_DESATIVADOS.index))
            RA_CONSOLIDADO = RA_CONSOLIDADO.append(RA_DESATIVADOS)

            continue

        del[[RA_ATIVADOS,RA_DESATIVADOS,arquivo_csv]]

        RA_CONSOLIDADO['data_solicitacao'] = RA_CONSOLIDADO['Moderação data de solicitação'].apply(str).apply(FuncoesGlobais.convSTRpDATA_SOLICITACAO)

        #######################################################################################################################################################################
        RA_CONSOLIDADO['Atribuido Para'] = RA_CONSOLIDADO['Atribuido Para'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Moderação motivo'] = RA_CONSOLIDADO['Moderação motivo'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Moderação status'] = RA_CONSOLIDADO['Moderação status'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})

        #######################################################################################################################################################################
        RA_CONSOLIDADO['Nível I - Empresa'] = RA_CONSOLIDADO['Nível I - Empresa'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Nível II - Motivos'] = RA_CONSOLIDADO['Nível II - Motivos'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})

        RA_CONSOLIDADO['Nível III - Acessórios / Lifestyle / Riders'] = RA_CONSOLIDADO['Nível III - Acessórios / Lifestyle / Riders'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Nível III - Atendimento'] = RA_CONSOLIDADO['Nível III - Atendimento'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Nível III - Financeiro'] = RA_CONSOLIDADO['Nível III - Financeiro'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Nível III - Institucional'] = RA_CONSOLIDADO['Nível III - Institucional'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Nível III - Peças'] = RA_CONSOLIDADO['Nível III - Peças'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Nível III - Processo de Compra'] = RA_CONSOLIDADO['Nível III - Processo de Compra'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Nível III - Produto'] = RA_CONSOLIDADO['Nível III - Produto'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Nível III - Recall'] = RA_CONSOLIDADO['Nível III - Recall'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Nível III - Serviços'] = RA_CONSOLIDADO['Nível III - Serviços'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Nível III - Tecnologia'] = RA_CONSOLIDADO['Nível III - Tecnologia'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})

        RA_CONSOLIDADO['Nível IV - Modelo Veículo BMW Brasil'] = RA_CONSOLIDADO['Nível IV - Modelo Veículo BMW Brasil'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Nível IV - Modelo Veículo BMW Motorrad'] = RA_CONSOLIDADO['Nível IV - Modelo Veículo BMW Motorrad'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        RA_CONSOLIDADO['Nível IV - Modelo Veículo MINI'] = RA_CONSOLIDADO['Nível IV - Modelo Veículo MINI'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        #######################################################################################################################################################################

        RA_CONSOLIDADO['Nível III'] = np.where(RA_CONSOLIDADO['Nível III - Tecnologia'] != 'N/I' ,RA_CONSOLIDADO['Nível III - Tecnologia'] ,RA_CONSOLIDADO['Nível III - Serviços'])
        RA_CONSOLIDADO['Nível III'] = np.where(RA_CONSOLIDADO['Nível III'] == 'N/I' ,RA_CONSOLIDADO['Nível III - Recall'] ,RA_CONSOLIDADO['Nível III'])
        RA_CONSOLIDADO['Nível III'] = np.where(RA_CONSOLIDADO['Nível III'] == 'N/I' ,RA_CONSOLIDADO['Nível III - Produto'] ,RA_CONSOLIDADO['Nível III'])
        RA_CONSOLIDADO['Nível III'] = np.where(RA_CONSOLIDADO['Nível III'] == 'N/I' ,RA_CONSOLIDADO['Nível III - Processo de Compra'] ,RA_CONSOLIDADO['Nível III'])
        RA_CONSOLIDADO['Nível III'] = np.where(RA_CONSOLIDADO['Nível III'] == 'N/I' ,RA_CONSOLIDADO['Nível III - Peças'] ,RA_CONSOLIDADO['Nível III'])
        RA_CONSOLIDADO['Nível III'] = np.where(RA_CONSOLIDADO['Nível III'] == 'N/I' ,RA_CONSOLIDADO['Nível III - Institucional'] ,RA_CONSOLIDADO['Nível III'])
        RA_CONSOLIDADO['Nível III'] = np.where(RA_CONSOLIDADO['Nível III'] == 'N/I' ,RA_CONSOLIDADO['Nível III - Financeiro'] ,RA_CONSOLIDADO['Nível III'])
        RA_CONSOLIDADO['Nível III'] = np.where(RA_CONSOLIDADO['Nível III'] == 'N/I' ,RA_CONSOLIDADO['Nível III - Atendimento'] ,RA_CONSOLIDADO['Nível III'])
        RA_CONSOLIDADO['Nível III'] = np.where(RA_CONSOLIDADO['Nível III'] == 'N/I' ,RA_CONSOLIDADO['Nível III - Acessórios / Lifestyle / Riders'] ,RA_CONSOLIDADO['Nível III'])
        #######################################################################

        RA_CONSOLIDADO['Nível IV'] = np.where(RA_CONSOLIDADO['Nível IV - Modelo Veículo MINI'] != 'N/I' ,RA_CONSOLIDADO['Nível IV - Modelo Veículo MINI'] ,RA_CONSOLIDADO['Nível IV - Modelo Veículo BMW Motorrad'])
        RA_CONSOLIDADO['Nível IV'] = np.where(RA_CONSOLIDADO['Nível IV'] == 'N/I' ,RA_CONSOLIDADO['Nível IV - Modelo Veículo BMW Brasil'] ,RA_CONSOLIDADO['Nível IV'])

        RA_CONSOLIDADO = RA_CONSOLIDADO.rename(columns={'Nível III': 'Nível III - Submotivo'
                                                       ,'Nível IV': 'Nível IV - Modelo'})

        RA_CONSOLIDADO = RA_CONSOLIDADO[['data_solicitacao','Atribuido Para','Id HugMe','Moderação data de solicitação','Moderação motivo','Moderação status',
                                         'Nível I - Empresa','Nível II - Motivos','Nível III - Submotivo','Nível IV - Modelo','Avaliações desconsideradas RA'
                                         ,'nome_base','nome_arquivo','registros']]




        #######################################################################################################################################################################


        # RA_CONSOLIDADO['Nível I'] = RA_CONSOLIDADO['Nível I'].replace({pd.NaT: 'Tabulacao Indefinida', np.NaN: 'Tabulacao Indefinida'})
        # RA_CONSOLIDADO['Nível II'] = RA_CONSOLIDADO['Nível II'].replace({pd.NaT: 'Tabulacao Indefinida', np.NaN: 'Tabulacao Indefinida'})
        # RA_CONSOLIDADO['Nível III'] = RA_CONSOLIDADO['Nível III'].replace({pd.NaT: 'Tabulacao Indefinida', np.NaN: 'Tabulacao Indefinida'})



        RA_CONSOLIDADO['semana'] = (RA_CONSOLIDADO['Moderação data de solicitação'].apply(str).apply(FuncoesGlobais.convDT_SEMANA))
        RA_CONSOLIDADO['ano'] = (RA_CONSOLIDADO['Moderação data de solicitação'].apply(str).apply(FuncoesGlobais.convDT_ANO))
        RA_CONSOLIDADO['num_mes'] = (RA_CONSOLIDADO['Moderação data de solicitação'].apply(str).apply(FuncoesGlobais.convDT_MES))

        RA_CONSOLIDADO = RA_CONSOLIDADO.merge(ListasAuxiliares.listAUX(), how='left', on='num_mes')
        RA_CONSOLIDADO.drop(['Moderação data de solicitação','num_mes'], axis=1, inplace=True)
        RA_CONSOLIDADO = RA_CONSOLIDADO.rename(columns={'nome_mes': 'mes'})
        RA_CONSOLIDADO.index = pd.RangeIndex(len(RA_CONSOLIDADO.index))

        return RA_CONSOLIDADO



if __name__ == "__main__":

    RA_MODERACOES = ExcelRA_MODERACOES.ExcelRA()