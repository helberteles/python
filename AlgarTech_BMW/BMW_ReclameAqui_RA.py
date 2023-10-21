import pandas as pd
import re, os
import numpy as np
import time
from datetime import date, datetime, timedelta
#pd.show_versions()

class PastasGenericas:

    ptRA = '//acsfs/DEPTOS/CPC/4 - MIS/2 - Cliente/36 - ReclameAqui/01 - BMW/RA/'

    ptDESATIVADOS = '//acsfs/DEPTOS/CPC/4 - MIS/2 - Cliente/36 - ReclameAqui/01 - BMW/RA Desativado/'

    ptFERIADOS = r'//acsfs/DEPTOS/CPC/4 - MIS/2 - Cliente/36 - ReclameAqui/01 - BMW/PyFeriados/Feriados.xlsx'

    ptSLA = '//acsfs/DEPTOS/CPC/4 - MIS/2 - Cliente/36 - ReclameAqui/01 - BMW/PySLA/'

class ListaGLOBAIS:

    def dfListaMESES():
        listMESES = [["01","01-JANEIRO"],["02","02-FEVEREIRO"],["03","03-MARÇO"],["04","04-ABRIL"],["05","05-MAIO"],["06","06-JUNHO"],["07","07-JULHO"],["08","08-AGOSTO"],["09","09-SETEMBRO"],["10","10-OUTUBRO"],["11","11-NOVEMBRO"],["12","12-DEZEMBRO"]]
        dfMESES = pd.DataFrame(data=listMESES,columns=['num_mes','nome_mes'])
        return dfMESES

    def dfListaREGIAO():
        dfREGIAO = [["AC","Norte"],
                    ["AL","Nordeste"],
                    ["AP","Norte"],
                    ["AM","Norte"],
                    ["BA","Nordeste"],
                    ["CE","Nordeste"],
                    ["DF","Centro-Oeste"],
                    ["ES","Sudeste"],
                    ["GO","Centro-Oeste"],
                    ["MA","Nordeste"],
                    ["MT","Centro-Oeste"],
                    ["MS","Centro-Oeste"],
                    ["MG","Sudeste"],
                    ["PA","Norte"],
                    ["PB","Nordeste"],
                    ["PR","Sul"],
                    ["PE","Nordeste"],
                    ["PI","Nordeste"],
                    ["RJ","Sudeste"],
                    ["RN","Nordeste"],
                    ["RS","Sul"],
                    ["RO","Norte"],
                    ["RR","Norte"],
                    ["SC","Sul"],
                    ["SP","Sudeste"],
                    ["SE","Nordeste"],
                    ["TO","Norte"]]
        dfREGIAO = pd.DataFrame(data=dfREGIAO,columns=['Estado','Região'])
        return dfREGIAO

class FuncoesGenericas:

    semana = ['2ª seg','3ª ter','4ª qua','5ª qui','6ª sex','7ª sab','1ª dom']
    semana_ddd = ['seg','ter','qua','qui','sex','sab','dom']
    def __string__ (self, semana, semana_ddd):

        self.semana = semana


    def convDT_ABREVIADA(self,string):
        try:
            retorno = format(datetime.strptime(string[:10],'%Y-%m-%d').date(),'%Y-%m-%d')
        except:

            retorno = None
        return retorno

    def replaceTIMESTAMP_DATE(self,string):
        try:
            vDATE_TIME = datetime.fromtimestamp(int(str(string)[:10]))
            vSUM_DAY = vDATE_TIME+timedelta(days=1)
            retorno = vSUM_DAY.strftime("%Y-%m-%d")

        except:
            try:
                if int(string[:4])>1900:
                    retorno = format(datetime.strptime(string[:10],'%Y-%m-%d').date(),'%Y-%m-%d')

                else:
                    retorno = None

            except:
                    retorno = None

        return retorno


    def converteIntervalo(self,string):
        if(string == None):
            retorno = None
        else:
            retorno = (string[11:])[:2]+":00:00"
        return retorno

    def convSEMANA(self,string):
        if(string == None):
            retorno = None
        else:
            retorno = self.semana[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]
        return retorno

    def convANO(self,string):
        if(string == None):
            retorno = None
        else:
            retorno = string[:4]
        return retorno

    def convMES(self,string):
        if(string == None):
            retorno = None
        else:
            retorno = string[5:7]
        return retorno

    def convDIA_SEMANA(self,string):
        if(string == None):
            retorno = None
        else:
            retorno = format(datetime.strptime(string[:10],'%Y-%m-%d').date(),'%d')+'-'+self.semana_ddd[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]
        return retorno

    def convFLOAT_INT(self,string):
        try:

            retorno = int((string).replace('.0',''))
        except:
            retorno = string
        return retorno

class FuncoesPersonalizadasSLA:

    h_inicio_sem = '08:00:00'
    h_fim_sem = '14:20:00'
    semana_lista = ['seg','ter','qua','qui','sex','sab','dom']

    temp_sem = 22800
    temp_sab = 22800
    temp_dom = 0
    tempo_semana = [temp_sem,temp_sem,temp_sem,temp_sem,temp_sem,temp_sab,temp_dom]


    temp_termino_sem = '14:20:00'
    temp_termino_sab = '14:20:00'
    temp_termino_dom = '14:20:00'
    temp_termino = [temp_termino_sem
                        ,temp_termino_sem
                        ,temp_termino_sem
                        ,temp_termino_sem
                        ,temp_termino_sem
                        ,temp_termino_sab
                        ,temp_termino_dom]

    temp_inicio_sem = '08:00:00'
    temp_inicio_sab = '08:00:00'
    temp_inicio_dom = '08:00:00'
    temp_inicio = [temp_inicio_sem
                        ,temp_inicio_sem
                        ,temp_inicio_sem
                        ,temp_inicio_sem
                        ,temp_inicio_sem
                        ,temp_inicio_sab
                        ,temp_inicio_dom]

    #---------------------------------------------------------------------------

    def __string__ (self, h_inicio_sem, h_fim_sem, semana_lista, tempo_semana, temp_termino):

        self.semana_lista = semana_lista
        self.h_inicio_sem = h_inicio_sem
        self.h_fim_sem = h_fim_sem

        self.tempo_semana = tempo_semana
        self.temp_termino =  temp_termino


    def convDT_RECLAMACAO_0(self,string):
        try:

            if ((self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='seg')
                    or (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='ter')
                    or (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='qua')
                    or (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='qui')
                    or (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='sex')
                    #or (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='sab')
                    ):
                    if (string >= string[:10]+' 00:00:00' and string < string[:10]+' '+str(self.h_inicio_sem)): #08:00:00
                        retorno = (date(*map(int, string[:10].split('-'))) +timedelta(days=0)).strftime("%Y-%m-%d")+' '+str(self.h_inicio_sem)  #mesmo dia últi com horario 8h

                    elif (string > string[:10]+' '+str(self.h_fim_sem) and string <= string[:10]+' 23:59:59'): #22:00:00
                        retorno = (date(*map(int, string[:10].split('-'))) +timedelta(days=1)).strftime("%Y-%m-%d")+' '+str(self.h_inicio_sem)
                    else:
                        retorno = string

            elif (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='sab'):

                if (string >= string[:10]+' 00:00:00' and string < string[:10]+' '+str(self.h_inicio_sem)): #08:00:00
                    retorno = (date(*map(int, string[:10].split('-'))) +timedelta(days=0)).strftime("%Y-%m-%d")+' '+str(self.h_inicio_sem)  #mesmo dia últi com horario 8h

                elif (string > string[:10]+' '+str(self.h_fim_sem) and string <= string[:10]+' 23:59:59'): #22:00:00
                    retorno = (date(*map(int, string[:10].split('-'))) +timedelta(days=2)).strftime("%Y-%m-%d")+' '+str(self.h_inicio_sem)
                else:
                    retorno = string

            elif (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='dom'):

                    retorno = (date(*map(int, string[:10].split('-'))) +timedelta(days=1)).strftime("%Y-%m-%d")+' '+str(self.h_inicio_sem)  #seg com horario 8h
            else:
                retorno = string
        except:
            retorno = None
#h_fim_sem
        return retorno

    def convDT_RESPOSTA_0(self,string):
        try:

            if ((self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='seg')
                    or (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='ter')
                    or (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='qua')
                    or (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='qui')
                    or (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='sex')
                    #or (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='sab')
                    ):
                    if (string >= string[:10]+' 00:00:00' and string < string[:10]+' '+str(self.h_inicio_sem)):   #08:00:00
                        retorno = (date(*map(int, string[:10].split('-'))) +timedelta(days=0)).strftime("%Y-%m-%d")+' '+str(self.h_fim_sem)  #mesmo dia últi com horario 14h

                    elif (string > string[:10]+' '+str(self.h_fim_sem) and string <= string[:10]+' 23:59:59'): #22:00:00
                        retorno = (date(*map(int, string[:10].split('-'))) +timedelta(days=0)).strftime("%Y-%m-%d")+' '+str(self.h_fim_sem)  #mesmo dia últi com horario 14h

                    else:
                        retorno = string

            elif (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='sab'):

                if (string >= string[:10]+' 00:00:00' and string < string[:10]+' '+str(self.h_inicio_sem)): #08:00:00
                    retorno = (date(*map(int, string[:10].split('-'))) +timedelta(days=0)).strftime("%Y-%m-%d")+' '+str(self.h_inicio_sem)  #mesmo dia últi com horario 8h

                elif (string > string[:10]+' '+str(self.h_fim_sem) and string <= string[:10]+' 23:59:59'): #22:00:00
                    retorno = (date(*map(int, string[:10].split('-'))) +timedelta(days=2)).strftime("%Y-%m-%d")+' '+str(self.h_inicio_sem)
                else:
                    retorno = string

            elif (self.semana_lista[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]=='dom'):

                    retorno = (date(*map(int, string[:10].split('-'))) +timedelta(days=1)).strftime("%Y-%m-%d")+' '+str(self.h_inicio_sem)  #seg com horario 8h
            else:
                retorno = string
        except:
            retorno = None
        return retorno




    def convSEMANA_TEMPO(self,string):
        if len(string)<5:
            retorno = 0
        else:
            retorno = self.tempo_semana[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]
        return retorno

    def convSEMANA_TEMPO_HORA(self,string):
        if len(string)<5:
            retorno = 0
        else:
            retorno = self.temp_termino[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]
        return retorno

    def transf_HORA_EM_SEGUNDOS(self,time_str):
        h, m, s = time_str.split(':') #formato 2019-08-01 20:00:00
        return int(h) * 3600 + int(m) * 60 + int(s)

    def transf_DT_HORA_EM_SEGUNDOS(self,time_str):
        h, m, s = time_str[11:].split(':') #formato 2019-08-01 20:00:00
        return int(h) * 3600 + int(m) * 60 + int(s)

    def convSEMANA_TEMPO_HORA_INICIO(self,string):
        if len(string)<5:
            retorno = 0
        else:
            retorno = self.temp_inicio[datetime.strptime(string[:10],'%Y-%m-%d').date().weekday()]
        return retorno

    def transf_DT_HORA_EM_SEGUNDOS_2(self,time_str):
        if len(time_str)<5:
            h = 0
            m = 0
            s = 0
        else:
            h, m, s = time_str[11:].split(':') #formato 2019-08-01 20:00:00
        return int(h) * 3600 + int(m) * 60 + int(s)

    def slaRESPOSTA(self,string):
        if len(string) == 4:
            retorno = 0
        else:
            retorno = 1
        return retorno

    def converteDate(self,stringDate):
        if(stringDate=="nan"):
            retorno = None
        else:
            retorno = (stringDate[8] + stringDate[9] +'/'+stringDate[5] + stringDate[6]+'/'+stringDate[:4]) #-formato dd-mm-yyyy
        return retorno

    def slaVERIFICAR(self,string):
        try:
            if int(string[:4])>=2000: #validados do campo ano
                retorno = 'nao_verificar'
            else:
                retorno = 'sim_verificar'
        except:
            retorno = 'sim_verificar'
        return retorno

class ExcelFeriados:

    def descFERIADOS():

        p = PastasGenericas

        dfFERIADOS = pd.read_excel(p.ptFERIADOS,encoding='latin_1')
        dfFERIADOS['dt_feriado_desconsiderar']='sim'
        return dfFERIADOS

class ExcelHistorico:

    def funcHistorico():
        p = PastasGenericas

        vLIST_ARQ = [os.path.join(p.ptSLA, nome) for nome in os.listdir(p.ptSLA)]
        vARQ_LIST = [arq for arq in vLIST_ARQ if os.path.isfile(arq)]
        vARQ_TIPO = [arq for arq in vARQ_LIST if arq.lower().endswith(".xlsx")]

        dfHISTORICO = pd.DataFrame()
        for arq in vARQ_TIPO:
            vUPLOAD = pd.read_excel(arq, encoding='latin_1') #header=None, skiprows = elimina linhas do df
            dfHISTORICO = dfHISTORICO.append(vUPLOAD)

        try:
            dfHISTORICO_VALIDADOR = dfHISTORICO[['Id HugMe','verificar_sla_novamente']]
            dfHISTORICO_VALIDADOR = dfHISTORICO_VALIDADOR.drop_duplicates(keep='last')
        except:
            dfHISTORICO_VALIDADOR = pd.DataFrame(columns=['Id HugMe','verificar_sla_novamente'])
            dfHISTORICO_VALIDADOR.index = pd.RangeIndex(len(dfHISTORICO_VALIDADOR.index))
        dfHISTORICO = dfHISTORICO_VALIDADOR

        del[[dfHISTORICO_VALIDADOR]]
        return dfHISTORICO

class ExcelRA_SLA:

    def excelReclameAqui():
        s = FuncoesPersonalizadasSLA() #quando usar o self tem que colocar entre colchetes
        f = FuncoesGenericas() #quando nao usar o self nao usar colchetes
        p = PastasGenericas

        h = ExcelHistorico
        dfHISTORICO = h.funcHistorico()
        dfHISTORICO = dfHISTORICO[dfHISTORICO['verificar_sla_novamente'] == 'sim_verificar']


        vLIST_ARQ = [os.path.join(p.ptRA, nome) for nome in os.listdir(p.ptRA)]
        vARQ_LIST = [arq for arq in vLIST_ARQ if os.path.isfile(arq)]
        vARQ_TIPO = [arq for arq in vARQ_LIST if arq.lower().endswith(".xlsx")]

        dfRA = pd.DataFrame()
        for arq in vARQ_TIPO:
            vUPLOAD = pd.read_excel(arq, encoding='latin_1', skiprows=3)
            dfRA['nome_arquivo'] = str(re.findall(r'RA/.*',arq)).replace(r'RA/','').replace("['",'').replace("']",'')
            dfRA = dfRA.append(vUPLOAD)
        dfRA = dfRA[['Id HugMe','Data Reclamação','Data de Resposta']]

        dfRA = dfRA.merge(dfHISTORICO, how='left', on='Id HugMe')

        dfRA['verificar_sla_novamente'] = dfRA['verificar_sla_novamente'].replace({pd.NaT: 'sim_verificar', np.NaN: 'sim_verificar'})
        dfRA = dfRA[dfRA['verificar_sla_novamente'] == 'sim_verificar']
        dfRA.drop(['verificar_sla_novamente'], axis=1, inplace=True) #--excluir coluna do dataframe

        dfRA['Data Reclamação'] = (dfRA['Data Reclamação'].apply(str).apply(s.convDT_RECLAMACAO_0))
        dfRA['Data de Resposta'] = (dfRA['Data de Resposta'].apply(str).apply(s.convDT_RESPOSTA_0))

        dfRA['data_reclamacao'] = (dfRA['Data Reclamação'].apply(str).apply(f.convDT_ABREVIADA))
        dfRA['data_resposta'] = (dfRA['Data de Resposta'].apply(str).apply(f.convDT_ABREVIADA))
        del[[dfHISTORICO]]
        return dfRA

class CalculoSLA:

    def execSLA():
        ##########################################
        r = ExcelRA_SLA
        dfUPLOAD = r.excelReclameAqui()

        ##########################################
        fr = ExcelFeriados
        dfFERIADOS = fr.descFERIADOS()
        dfFERIADOS['dt_feriado_desconsiderar']='sim'

        ##########################################
        #f = FuncoesGenericas #quando nao usar o self nao usar colchetes
        f = FuncoesGenericas() #quando nao usar o self nao usar colchetes
        s = FuncoesPersonalizadasSLA() #quando usar o self tem que colocar entre colchetes

        ##########################################
        p = PastasGenericas

        #STEP_1############################################################################################################################################
        dfUPLOAD['dias_reclamacao_resposta'] = ''
        linha = len(dfUPLOAD['Data Reclamação']) #gera contagem da quantidade datas
        v = 0

        #popula os dias da coluna 'dias_reclamacao_resposta'
        while v < linha:
            try:
                vRECLAMACAO = dfUPLOAD.iloc[v,3] #data_reclamacao
                vRECLAMACAO = date(*map(int, vRECLAMACAO.split('-')))
                vRESPOSTA = dfUPLOAD.iloc[v,4] #data_resposta
                vRESPOSTA = date(*map(int, vRESPOSTA.split('-')))

                dfUPLOAD.iloc[v,5] = abs((vRECLAMACAO - vRESPOSTA).days) #dias_reclamacao_resposta
            except:
                dfUPLOAD.iloc[v,5] = 0 #dias_reclamacao_resposta
            v = v + 1

        #STEP_2############################################################################################################################################
        vMAX_COLUNA = dfUPLOAD['dias_reclamacao_resposta'].values.max() #verifica qual é a meior quantidade de datas na coluna
        v = 0
        while v < vMAX_COLUNA:#gera colunas df
            dfUPLOAD['coluna_data_'+str(v)] = ''
            v = v + 1

        #STEP_2############################################################################################################################################
        #insere datas nas colunas e verifica se é semana ou final de semana
        vLINHA_FINAL = len(dfUPLOAD['Data Reclamação'])
        vLINHA_INICIAL = 0
        #obtem parametros da coluna
        COLUNAS_DF = dfUPLOAD.columns.values
        vNOME_COLUNA_DF = pd.DataFrame(data=COLUNAS_DF,columns=['nome_coluna']) #transforma coluna em df
        vMAX_INDICE_COL = len(vNOME_COLUNA_DF.index) #conta a quantidade de linhas
        vCOLUNA_INICIO = (vMAX_INDICE_COL - vMAX_COLUNA) #faz a diferença entre o máximo de colunas e a coluna_data_(numero)
        #popula informações de data por coluna (processo que consome mais tempo)
        while vLINHA_INICIAL < vLINHA_FINAL: #corre linha

            try:
                vRECLAMACAO = dfUPLOAD.iloc[vLINHA_INICIAL,3] #obtem o resultado de DtReclamação com base na linha
                vRECLAMACAO = date(*map(int, vRECLAMACAO.split('-'))) #transforma o resultado de DtReclamação em data
                vRESPOSTA = dfUPLOAD.iloc[vLINHA_INICIAL,4] #obtem o resultado de DtResposta com base na linha
                vRESPOSTA = date(*map(int, vRESPOSTA.split('-'))) #transforma o resultado de DtResposta em data
                vFREQ_DATA = pd.date_range(vRECLAMACAO,vRESPOSTA,freq='D') #obtem a frequência entre a data reclamação vs resposta
                vFREQ_FINAL = pd.DataFrame(data=vFREQ_DATA,columns=['nome_coluna'])#frequencia de colunas

                vFREQ_FINAL = len(vFREQ_FINAL.index) #conta a quantidade de linhas
                vCOLUNA_INICIO = 6 #coluna que inicia a inserção de dados
                vCOLUNA_FINAL = (vCOLUNA_INICIO + vFREQ_FINAL)

                while vCOLUNA_INICIO < vCOLUNA_FINAL: #corre coluna conforme posição

                    try:
                        vFREQ_DATA_1 = pd.DataFrame(data=vFREQ_DATA).iloc[(vCOLUNA_INICIO-6),0] #
                        dfUPLOAD.iloc[vLINHA_INICIAL,vCOLUNA_INICIO] = vFREQ_DATA_1 #linha,coluna (registra o resultado com base na coluna correspondente)
                        #print('saiu try '+str(vCOLUNA_INICIO))
                        vCOLUNA_INICIO = vCOLUNA_INICIO + 1
                        #print('adicionou coluna'+ str(vCOLUNA_INICIO))
                    except:
                        vCOLUNA_INICIO = vCOLUNA_FINAL
                        #print('entrou no except '+str(vCOLUNA_INICIO))
                    continue

                #print('linha atual: '+str(vLINHA_INICIAL))
                vLINHA_INICIAL = vLINHA_INICIAL + 1

            except:
                vLINHA_INICIAL = vLINHA_INICIAL + 1


        #STEP_3############################################################################################################################################
        #remove as datas indesejadas
        vMAX_LINHA = len(dfUPLOAD['Id HugMe'])
        vCOLUNA_INICIO = 6
        vCOLUNA_FINAL = (vCOLUNA_INICIO + vMAX_COLUNA)

        vDTEXPURGO_FIM = len(dfFERIADOS['data'])
        vDTEXPURGO_INICIO = 0

        while vCOLUNA_INICIO < vCOLUNA_FINAL:
            vDTEXPURGO_INICIO = 0
            while vDTEXPURGO_INICIO < vDTEXPURGO_FIM:
                dfUPLOAD.iloc[0:vMAX_LINHA,vCOLUNA_INICIO:vCOLUNA_INICIO+1] = dfUPLOAD.iloc[0:vMAX_LINHA,vCOLUNA_INICIO:vCOLUNA_INICIO+1].replace(dfFERIADOS.iloc[vDTEXPURGO_INICIO,0],'')

                vDTEXPURGO_INICIO = vDTEXPURGO_INICIO +1

            vCOLUNA_INICIO = vCOLUNA_INICIO +1


        #STEP_4############################################################################################################################################
        vMAX_COLUNA = dfUPLOAD['dias_reclamacao_resposta'].values.max() #verifica qual é a maior quantidade de datas na coluna
        v = 0
        while v < vMAX_COLUNA: #gera colunas de data df
            dfUPLOAD['coluna_data_'+str(v)] = dfUPLOAD['coluna_data_'+str(v)].apply(str).apply(f.replaceTIMESTAMP_DATE)
            v = v + 1


        #STEP_5############################################################################################################################################
        #Aplica conversão por coluna de tempo---------------------------
        vMAX_LINHA = len(dfUPLOAD['Id HugMe'])
        vCOLUNA_INICIO = 6
        vCOLUNA_FINAL = (vCOLUNA_INICIO + vMAX_COLUNA)
        dfUPLOAD['coluna_auxiliar'] = ''
        while vCOLUNA_INICIO < vCOLUNA_FINAL:

            dfUPLOAD['coluna_auxiliar'] = dfUPLOAD.iloc[0:vMAX_LINHA,vCOLUNA_INICIO:vCOLUNA_INICIO+1]
            dfUPLOAD['coluna_auxiliar'] = (dfUPLOAD['coluna_auxiliar'].apply(str).apply(s.convSEMANA_TEMPO))
            dfUPLOAD.iloc[0:vMAX_LINHA,vCOLUNA_INICIO:vCOLUNA_INICIO+1] = dfUPLOAD['coluna_auxiliar']

            vCOLUNA_INICIO = vCOLUNA_INICIO +1

        dfUPLOAD.drop(['coluna_auxiliar'], axis=1, inplace=True) #--excluir coluna do dataframe


        #STEP_6############################################################################################################################################
        #aplica somatoria acumulativa dos tempos de todos os dias
        vMAX_LINHA = len(dfUPLOAD['Id HugMe'])
        vCOLUNA_INICIO = 6
        vCOLUNA_FINAL = (vCOLUNA_INICIO + vMAX_COLUNA)
        dfUPLOAD['coluna_acumulativa'] = 0
        dfUPLOAD['coluna_auxiliar'] =''
        while vCOLUNA_INICIO < vCOLUNA_FINAL:

            dfUPLOAD['coluna_auxiliar'] = dfUPLOAD.iloc[0:vMAX_LINHA,vCOLUNA_INICIO:vCOLUNA_INICIO+1]
            dfUPLOAD['coluna_acumulativa'] = (dfUPLOAD['coluna_acumulativa'] + dfUPLOAD['coluna_auxiliar'])

            vCOLUNA_INICIO = vCOLUNA_INICIO +1


        dfUPLOAD['sla_horas_acumuladas'] = dfUPLOAD['coluna_acumulativa']
        dfUPLOAD.drop(['coluna_auxiliar','coluna_acumulativa'], axis=1, inplace=True) #dropa coluna auxiliar que não é utilizada

        #STEP_7############################################################################################################################################
        #dias considerados
        vMAX_LINHA = len(dfUPLOAD['Id HugMe'])
        vCOLUNA_INICIO = 6
        vMAX_COLUNA_2 = len(list(dfUPLOAD))-1 # faz a leitura do número de colunas
        vCOLUNA_FINAL = vMAX_COLUNA_2 #seleciona a coluna final
        dfUPLOAD['dias_reclamacao_resposta_aux_acumulativa'] = 0

        while vCOLUNA_INICIO < vCOLUNA_FINAL:

            dfUPLOAD['dias_reclamacao_resposta_aux'] = np.where(dfUPLOAD.iloc[0:vMAX_LINHA,vCOLUNA_INICIO:vCOLUNA_INICIO+1] == int(s.temp_sem),1,0)
            dfUPLOAD['dias_reclamacao_resposta_aux_acumulativa'] = (dfUPLOAD['dias_reclamacao_resposta_aux_acumulativa'] + dfUPLOAD['dias_reclamacao_resposta_aux'])

            vCOLUNA_INICIO = vCOLUNA_INICIO +1

        dfUPLOAD['dias_reclamacao_desconsiderados'] = (dfUPLOAD['dias_reclamacao_resposta'] - dfUPLOAD['dias_reclamacao_resposta_aux_acumulativa'])
        dfUPLOAD['dias_reclamacao_desconsiderados'] = np.where(dfUPLOAD['dias_reclamacao_desconsiderados'] < 1,0,dfUPLOAD['dias_reclamacao_desconsiderados'])
        dfUPLOAD = dfUPLOAD[['Id HugMe','Data Reclamação','Data de Resposta','data_reclamacao','data_resposta','dias_reclamacao_resposta','sla_horas_acumuladas','dias_reclamacao_desconsiderados']] #seleciona as colunas a serem utilizadas


        #STEP_8############################################################################################################################################
        #CALCULO DA DT_RECLAMAÇÃO (separa o tempo a ser utilizado)
        pd.options.mode.chained_assignment = None #silencia mensagens python
        dfUPLOAD['dt_reclamacao_horario_plan'] = (dfUPLOAD['data_reclamacao'].apply(str).apply(s.convSEMANA_TEMPO)) #Converte data em tempo, conforme o dia da semana ao qual corresponde (semana ou sáb)
        dfUPLOAD['dt_resposta_horario_plan'] = (dfUPLOAD['data_resposta'].apply(str).apply(s.convSEMANA_TEMPO)) #Converte data em tempo, conforme o dia da semana ao qual corresponde (semana ou sáb)
        dfUPLOAD['soma_tempo_reclamacao_resposta'] = np.where(dfUPLOAD['dias_reclamacao_resposta'] <= 1,0,(dfUPLOAD['dt_reclamacao_horario_plan']+dfUPLOAD['dt_resposta_horario_plan']))#soma tempo reclamação e resposta
        dfUPLOAD['dif_tempo_reclamacao_resposta_acumulativa'] = np.where(dfUPLOAD['soma_tempo_reclamacao_resposta']==0,0,(dfUPLOAD['sla_horas_acumuladas'] - dfUPLOAD['soma_tempo_reclamacao_resposta']))#subtrai o resultado do montante versus a dt_reclamação e dt_resposta
        dfUPLOAD.drop(['dt_reclamacao_horario_plan','dt_resposta_horario_plan','soma_tempo_reclamacao_resposta','sla_horas_acumuladas'], axis=1, inplace=True) #dropa coluna auxiliar que não é utilizada


        #STEP_9############################################################################################################################################
        #gera a diferença de tempo data_reclamacao versus hora limite funcionamento operação
        dfUPLOAD['limite_tempo_reclamacao'] = (dfUPLOAD['data_reclamacao'].apply(str).apply(s.convSEMANA_TEMPO_HORA)) #hora máxima da reclamação
        dfUPLOAD['limite_tempo_reclamacao'] = (dfUPLOAD['limite_tempo_reclamacao'].apply(str).apply(s.transf_HORA_EM_SEGUNDOS)) #transforma essa hora maxima em segundos
        dfUPLOAD['dt_reclamacao_segundos'] = (dfUPLOAD['Data Reclamação'].apply(str).apply(s.transf_DT_HORA_EM_SEGUNDOS))
        dfUPLOAD['dif_tempo_reclamacao'] = (dfUPLOAD['limite_tempo_reclamacao'] - dfUPLOAD['dt_reclamacao_segundos'])
        dfUPLOAD['dif_tempo_reclamacao'] = np.where(dfUPLOAD['dt_reclamacao_segundos']>dfUPLOAD['limite_tempo_reclamacao']
                                                   ,dfUPLOAD['dt_reclamacao_segundos']-dfUPLOAD['limite_tempo_reclamacao']
                                                   ,dfUPLOAD['limite_tempo_reclamacao']-dfUPLOAD['dt_reclamacao_segundos'])
        dfUPLOAD.drop(['limite_tempo_reclamacao'], axis=1, inplace=True) #dropa coluna auxiliar que não é utilizada

        #STEP_10############################################################################################################################################
        #gera a diferença de tempo data_resposta versus hora limite funcionamento operação
        dfUPLOAD['limite_tempo_resposta'] = (dfUPLOAD['data_resposta'].apply(str).apply(s.convSEMANA_TEMPO_HORA_INICIO))
        dfUPLOAD['limite_tempo_resposta'] = np.where(dfUPLOAD['limite_tempo_resposta']==0,'00:00:00',dfUPLOAD['limite_tempo_resposta'])
        dfUPLOAD['limite_tempo_resposta'] = (dfUPLOAD['limite_tempo_resposta'].apply(str).apply(s.transf_HORA_EM_SEGUNDOS))
        dfUPLOAD['dt_resposta_segundos'] = (dfUPLOAD['Data de Resposta'].apply(str).apply(s.transf_DT_HORA_EM_SEGUNDOS_2))
        dfUPLOAD['dif_tempo_resposta'] = (dfUPLOAD['dt_resposta_segundos']-dfUPLOAD['limite_tempo_resposta'])
        dfUPLOAD['dif_tempo_resposta'] = np.where(dfUPLOAD['limite_tempo_resposta']>dfUPLOAD['dt_resposta_segundos']
                                                   ,dfUPLOAD['limite_tempo_resposta']-dfUPLOAD['dt_resposta_segundos']
                                                   ,dfUPLOAD['dt_resposta_segundos']-dfUPLOAD['limite_tempo_resposta'])
        dfUPLOAD.drop(['limite_tempo_resposta'], axis=1, inplace=True) #dropa coluna auxiliar que não é utilizada



        #STEP_11############################################################################################################################################
        dfUPLOAD['sla_tempo_resposta'] = np.where(dfUPLOAD['data_reclamacao'] == dfUPLOAD['data_resposta'],
        (dfUPLOAD['dt_resposta_segundos']-dfUPLOAD['dt_reclamacao_segundos']),
        (dfUPLOAD['dif_tempo_reclamacao_resposta_acumulativa']+dfUPLOAD['dif_tempo_reclamacao']+dfUPLOAD['dif_tempo_resposta']))

        dfUPLOAD['sla_tempo_resposta'] = np.where(dfUPLOAD['sla_tempo_resposta']<0,0,dfUPLOAD['sla_tempo_resposta'])
        dfUPLOAD['registros']= np.where(dfUPLOAD['sla_tempo_resposta']==0,0,1)

        dfUPLOAD['coluna_aux'] = (dfUPLOAD['data_resposta'].apply(str).apply(s.slaRESPOSTA))
        dfUPLOAD['sla_tempo_resposta']= np.where(dfUPLOAD['coluna_aux']== 0,0,dfUPLOAD['sla_tempo_resposta'])
        dfUPLOAD['sla_tempo_resposta']= np.where(dfUPLOAD['data_resposta']==None,0,dfUPLOAD['sla_tempo_resposta'])
        dfUPLOAD['data'] = (dfUPLOAD['Data Reclamação'].apply(str).apply(s.converteDate))


        #STEP_12############################################################################################################################################
        dfUPLOAD.drop(['data_reclamacao','data_resposta','dt_reclamacao_segundos','dt_resposta_segundos','data'], axis=1, inplace=True) #--excluir coluna do dataframe
        dfUPLOAD.drop(['dif_tempo_reclamacao_resposta_acumulativa','dif_tempo_reclamacao','dif_tempo_resposta'], axis=1, inplace=True) #dropa coluna auxiliar que não é utilizada

        dfUPLOAD['verificar_sla_novamente'] = dfUPLOAD['Data de Resposta'].apply(str).apply(s.slaVERIFICAR)
        dfUPLOAD = dfUPLOAD.drop_duplicates(keep='last')
        dfUPLOAD.index = pd.RangeIndex(len(dfUPLOAD.index))
        dfUPLOAD.to_excel(str(p.ptSLA)+'RA_historico_'+ str(datetime.now().strftime('%d-%m-%Y_%H%M%S')) +'.xlsx', index=False, encoding='latin_1')
        del[[dfFERIADOS,dfUPLOAD,vNOME_COLUNA_DF]]

class ReclameAqui:

    def readSLA():

        p = PastasGenericas

        vLISTA = [os.path.join(str(p.ptSLA), nome) for nome in os.listdir(str(p.ptSLA))]
        vARQ_LIST = [arq for arq in vLISTA if os.path.isfile(arq)]
        vARQ_TIPO = [arq for arq in vARQ_LIST if arq.lower().endswith(".xlsx")]
        dfSLA = pd.DataFrame()
        for arq in vARQ_TIPO:
            vUPLOAD = pd.read_excel(arq, encoding='latin_1') #header=None, skiprows = elimina linhas do df
            dfSLA = dfSLA.append(vUPLOAD)

        dfSLA = dfSLA.drop_duplicates(keep='last')
        dfSLA.drop(['coluna_aux','verificar_sla_novamente'], axis=1, inplace=True) #dropa coluna auxiliar que não é utilizada
        dfSLA.index = pd.RangeIndex(len(dfSLA.index))
        del[[vUPLOAD]]
        return dfSLA

    def readDesativados():
        p = PastasGenericas
        f = FuncoesGenericas() #quando nao usar o self nao usar colchetes
        s = FuncoesPersonalizadasSLA() #quando usar o self tem que colocar entre colchetes

        dfMESES = ListaGLOBAIS.dfListaMESES()
        dfREGIAO = ListaGLOBAIS.dfListaREGIAO()

        vLISTA = [os.path.join(str(p.ptDESATIVADOS), nome) for nome in os.listdir(str(p.ptDESATIVADOS))]
        vARQ_LIST = [arq for arq in vLISTA if os.path.isfile(arq)]
        vARQ_TIPO = [arq for arq in vARQ_LIST if arq.lower().endswith(".xlsx")]

        dfDESATIVADOS = pd.DataFrame()
        for arq in vARQ_TIPO:
            vUPLOAD = pd.read_excel(arq, encoding='latin_1', skiprows=3) #header=None, skiprows = elimina linhas do df
            vUPLOAD['nome_arquivo'] = str(re.findall(r'RA Desativado/.*',arq)).replace(r'RA Desativado/','').replace("['",'').replace("']",'')
            dfDESATIVADOS = dfDESATIVADOS.append(vUPLOAD)

        dfDESATIVADOS[['Data Reclamação SLA','Data de Resposta SLA','Qual o melhor horário para falar com você?'
                      ,'data','intervalo','semana','ano','num_mes','nome_mes','País','origem_ra_padrao','dia_semana'
                      ,'sla_tempo_resposta','registros','tipo_base'
                      ]] = pd.DataFrame([[np.nan, np.nan, np.nan,
                                          np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                                          np.nan, 1, 'RA_DESATIVADOS'
                              ]], index=dfDESATIVADOS.index)

        dfDESATIVADOS['data'] = (dfDESATIVADOS['Data Reclamação'].apply(str).apply(s.converteDate))
        dfDESATIVADOS['intervalo'] = (dfDESATIVADOS['Data Reclamação'].apply(str).apply(f.converteIntervalo))
        dfDESATIVADOS['semana'] = (dfDESATIVADOS['Data Reclamação'].apply(str).apply(f.convSEMANA))
        dfDESATIVADOS['ano'] = (dfDESATIVADOS['Data Reclamação'].apply(str).apply(f.convANO))
        dfDESATIVADOS['num_mes'] = (dfDESATIVADOS['Data Reclamação'].apply(str).apply(f.convMES))
        dfDESATIVADOS['dia_semana'] = (dfDESATIVADOS['Data Reclamação'].apply(str).apply(f.convDIA_SEMANA))
        #------------------------------------------------------------------------------------------
        dfDESATIVADOS = dfDESATIVADOS[dfDESATIVADOS['Avaliações desconsideradas RA'] == 'não']
        dfDESATIVADOS = dfDESATIVADOS.merge(dfMESES, how='left', on='num_mes')
        dfDESATIVADOS = dfDESATIVADOS.merge(dfREGIAO, how='left', on='Estado')
        dfDESATIVADOS['nome_mes'] = dfDESATIVADOS['nome_mes_y']
        dfDESATIVADOS.drop(['nome_mes_x','nome_mes_y'], axis=1, inplace=True) #--excluir coluna do dataframe
        #------------------------------------------------------------------------------------------
        dfDESATIVADOS = dfDESATIVADOS[['Atribuido Para','Arquivado ?','Congelado?','Origem RA','Status RA','Status Hugme','RG','Email','Cidade','Nome',
        'Avaliacao Favoravel ','Avaliações desconsideradas RA','Avaliado sem resposta RA','Título','Texto da Reclamação','Moderação motivo','Moderação status','Moderação usuário que solicitou','Seu problema foi resolvido?','Estado',
        'Telefones','CPF/CNPJ','Tempo primeira resposta (privado)','Tempo primeira resposta (público)','Id Origem','Id HugMe','Nota','Data de Resposta','Réplicas na reclamação RA','Quantidade interações consumidor',
        'Quantidade interações empresa','Mensagens internas neste ticket','Data Avaliacao','Data da última modificação','Tags','Nível I - Empresa','Nível II - Motivos','Nível III - Acessórios / Lifestyle / Riders','Nível III - Atendimento','Nível III - Financeiro',
        'Nível III - Institucional','Nível III - Peças','Nível III - Processo de Compra','Nível III - Produto','Nível III - Recall','Nível III - Serviços','Nível III - Tecnologia','Nível IV - Modelo Veículo BMW Brasil','Nível IV - Modelo Veículo BMW Motorrad','Nível IV - Modelo Veículo MINI',
        'Data fechamento','Data Reclamação','Data última réplica','Moderação data da resposta','Moderação data de solicitação','Redistribuições','Moderações neste ticket','Data Consideração Consumidor','Quantidade de lembretes','Comentários na reclamação*',
        'Data Consideração Empresa','Consideração Empresa','Tempo Avaliação','Data de Desativação RA','Motivo de Desativação RA','Categorias - FaleConosco','Motivo da Reclamação RA','Blackfriday RA','Sentimento','Dados Complementares Consumidor',
        'Sentimento RA*','Quantidade de Tags','Origem','Quantidade de Atribuições','Pessoa Física ou Jurídica?','Interações neste ticket','Tipo Hugme','Resposta da empresa','Voltaria a fazer negócio?','Consideração Consumidor',
        'Feed tipo','Fonte informação tipo','RA Prime','data','intervalo','semana','ano','num_mes','dia_semana','nome_mes',
        'Região','tipo_base','registros','Data Reclamação SLA','Data de Resposta SLA','sla_tempo_resposta','nome_arquivo']]


        dfDESATIVADOS = dfDESATIVADOS.drop_duplicates(keep='last')
        dfDESATIVADOS.index = pd.RangeIndex(len(dfDESATIVADOS.index))
        del[[vUPLOAD]]
        return dfDESATIVADOS

    def readRA():
        p = PastasGenericas
        f = FuncoesGenericas() #quando nao usar o self nao usar colchetes
        s = FuncoesPersonalizadasSLA() #quando usar o self tem que colocar entre colchetes

        dfMESES = ListaGLOBAIS.dfListaMESES()
        dfREGIAO = ListaGLOBAIS.dfListaREGIAO()

        vLISTA = [os.path.join(str(p.ptRA), nome) for nome in os.listdir(str(p.ptRA))]
        vARQ_LIST = [arq for arq in vLISTA if os.path.isfile(arq)]
        vARQ_TIPO = [arq for arq in vARQ_LIST if arq.lower().endswith(".xlsx")]
        dfRA = pd.DataFrame()
        for arq in vARQ_TIPO:
            vUPLOAD = pd.read_excel(arq, encoding='latin_1', skiprows=3) #header=None, skiprows = elimina linhas do df
            vUPLOAD['nome_arquivo'] = str(re.findall(r'RA/.*',arq)).replace(r'RA/','').replace("['",'').replace("']",'')
            dfRA = dfRA.append(vUPLOAD)

        dfRA = dfRA[dfRA['Avaliações desconsideradas RA'] == 'não']
        pd.options.mode.chained_assignment = None #silencia mensagens python
        dfRA['data'] = (dfRA['Data Reclamação'].apply(str).apply(s.converteDate))
        dfRA['intervalo'] = (dfRA['Data Reclamação'].apply(str).apply(f.converteIntervalo))
        dfRA['semana'] = (dfRA['Data Reclamação'].apply(str).apply(f.convSEMANA))
        dfRA['ano'] = (dfRA['Data Reclamação'].apply(str).apply(f.convANO))
        dfRA['num_mes'] = (dfRA['Data Reclamação'].apply(str).apply(f.convMES))
        dfRA['dia_semana'] = (dfRA['Data Reclamação'].apply(str).apply(f.convDIA_SEMANA))
        #------------------------------------------------------------------------------------------
        dfRA = dfRA.merge(dfMESES, how='left', on='num_mes')
        dfRA = dfRA.merge(dfREGIAO, how='left', on='Estado')
        dfRA['tipo_base']='RA'
        dfRA['registros']=1
        #------------------------------------------------------------------------------------------
        dfRA[['Data Reclamação SLA','Data de Resposta SLA','sla_tempo_resposta']] = pd.DataFrame([[np.nan, np.nan, np.nan]], index=dfRA.index)
        dfRA = dfRA[['Atribuido Para','Arquivado ?','Congelado?','Origem RA','Status RA','Status Hugme','RG','Email','Cidade','Nome',
        'Avaliacao Favoravel ','Avaliações desconsideradas RA','Avaliado sem resposta RA','Título','Texto da Reclamação','Moderação motivo','Moderação status','Moderação usuário que solicitou','Seu problema foi resolvido?','Estado',
        'Telefones','CPF/CNPJ','Tempo primeira resposta (privado)','Tempo primeira resposta (público)','Id Origem','Id HugMe','Nota','Data de Resposta','Réplicas na reclamação RA','Quantidade interações consumidor',
        'Quantidade interações empresa','Mensagens internas neste ticket','Data Avaliacao','Data da última modificação','Tags','Nível I - Empresa','Nível II - Motivos','Nível III - Acessórios / Lifestyle / Riders','Nível III - Atendimento','Nível III - Financeiro',
        'Nível III - Institucional','Nível III - Peças','Nível III - Processo de Compra','Nível III - Produto','Nível III - Recall','Nível III - Serviços','Nível III - Tecnologia','Nível IV - Modelo Veículo BMW Brasil','Nível IV - Modelo Veículo BMW Motorrad','Nível IV - Modelo Veículo MINI',
        'Data fechamento','Data Reclamação','Data última réplica','Moderação data da resposta','Moderação data de solicitação','Redistribuições','Moderações neste ticket','Data Consideração Consumidor','Quantidade de lembretes','Comentários na reclamação*',
        'Data Consideração Empresa','Consideração Empresa','Tempo Avaliação','Data de Desativação RA','Motivo de Desativação RA','Categorias - FaleConosco','Motivo da Reclamação RA','Blackfriday RA','Sentimento','Dados Complementares Consumidor',
        'Sentimento RA*','Quantidade de Tags','Origem','Quantidade de Atribuições','Pessoa Física ou Jurídica?','Interações neste ticket','Tipo Hugme','Resposta da empresa','Voltaria a fazer negócio?','Consideração Consumidor',
        'Feed tipo','Fonte informação tipo','RA Prime','data','intervalo','semana','ano','num_mes','dia_semana','nome_mes',
        'Região','tipo_base','registros','Data Reclamação SLA','Data de Resposta SLA','sla_tempo_resposta','nome_arquivo']]
        dfRA = dfRA.drop_duplicates(keep='last')
        dfRA.index = pd.RangeIndex(len(dfRA.index))
        del[[vUPLOAD]]
        return dfRA

class MergeReclameAqui:

    def mergeRA():
        f = FuncoesGenericas() #quando nao usar o self nao usar colchetes
        CalculoSLA.execSLA()
        dfSLA = ReclameAqui.readSLA()
        dfDesativados = ReclameAqui.readDesativados()
        dfRA = ReclameAqui.readRA()
        #######################################################################
        dfRA = [dfRA,dfDesativados]
        dfRA = pd.concat(dfRA)
        #######################################################################
        dfSLA = dfSLA.rename(columns={'Data Reclamação': 'Data Reclamação SLA'
                                     ,'Data de Resposta': 'Data de Resposta SLA'
                                     })

        dfRA = dfRA.merge(dfSLA, how='left', on='Id HugMe')
        #######################################################################

        dfRA.drop(['registros_y','Data Reclamação SLA_x','Data de Resposta SLA_x','sla_tempo_resposta_x'], axis=1, inplace=True)
        dfRA = dfRA.rename(columns={'registros_x': 'registros'
                                     ,'Data Reclamação SLA_y': 'Data Reclamação SLA'
                                     ,'Data de Resposta SLA_y': 'Data de Resposta SLA'
                                     ,'sla_tempo_resposta_y': 'sla_tempo_resposta'
                                     ,'Nível I - Empresa' : 'Nível I'
                                     ,'Nível II - Motivos' : 'Nível II'
                                     })

        #######################################################################
        dfRA['Estado'] = dfRA['Estado'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Cidade'] = dfRA['Cidade'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Região'] = dfRA['Região'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nome'] = dfRA['Nome'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Atribuido Para'] = dfRA['Atribuido Para'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Voltaria a fazer negócio?'] = dfRA['Voltaria a fazer negócio?'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Status RA'] = dfRA['Status RA'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Moderação motivo'] = dfRA['Moderação motivo'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Moderação status'] = dfRA['Moderação status'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})

        #######################################################################
        dfRA['Tags'] = dfRA['Tags'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nível I'] = dfRA['Nível I'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nível II'] = dfRA['Nível II'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})

        dfRA['Nível III - Acessórios / Lifestyle / Riders'] = dfRA['Nível III - Acessórios / Lifestyle / Riders'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nível III - Atendimento'] = dfRA['Nível III - Atendimento'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nível III - Financeiro'] = dfRA['Nível III - Financeiro'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nível III - Institucional'] = dfRA['Nível III - Institucional'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nível III - Peças'] = dfRA['Nível III - Peças'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nível III - Processo de Compra'] = dfRA['Nível III - Processo de Compra'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nível III - Produto'] = dfRA['Nível III - Produto'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nível III - Recall'] = dfRA['Nível III - Recall'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nível III - Serviços'] = dfRA['Nível III - Serviços'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nível III - Tecnologia'] = dfRA['Nível III - Tecnologia'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})

        dfRA['Nível IV - Modelo Veículo BMW Brasil'] = dfRA['Nível IV - Modelo Veículo BMW Brasil'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nível IV - Modelo Veículo BMW Motorrad'] = dfRA['Nível IV - Modelo Veículo BMW Motorrad'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        dfRA['Nível IV - Modelo Veículo MINI'] = dfRA['Nível IV - Modelo Veículo MINI'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        #######################################################################

        dfRA['dias_reclamacao_resposta'] = dfRA['dias_reclamacao_resposta'].apply(str).apply(f.convFLOAT_INT)
        dfRA['dias_reclamacao_desconsiderados'] = dfRA['dias_reclamacao_desconsiderados'].apply(str).apply(f.convFLOAT_INT)
        dfRA['sla_tempo_resposta'] = dfRA['sla_tempo_resposta'].apply(str).apply(f.convFLOAT_INT)
        dfRA['Nota'] = dfRA['Nota'].apply(str).apply(f.convFLOAT_INT)


        #######################################################################

        dfRA['Nível III'] = np.where(dfRA['Nível III - Tecnologia'] != 'N/I' ,dfRA['Nível III - Tecnologia'] ,dfRA['Nível III - Serviços'] )
        dfRA['Nível III'] = np.where(dfRA['Nível III'] == 'N/I' ,dfRA['Nível III - Recall'] ,dfRA['Nível III'])
        dfRA['Nível III'] = np.where(dfRA['Nível III'] == 'N/I' ,dfRA['Nível III - Produto'] ,dfRA['Nível III'])
        dfRA['Nível III'] = np.where(dfRA['Nível III'] == 'N/I' ,dfRA['Nível III - Processo de Compra'] ,dfRA['Nível III'])
        dfRA['Nível III'] = np.where(dfRA['Nível III'] == 'N/I' ,dfRA['Nível III - Peças'] ,dfRA['Nível III'])
        dfRA['Nível III'] = np.where(dfRA['Nível III'] == 'N/I' ,dfRA['Nível III - Institucional'] ,dfRA['Nível III'])
        dfRA['Nível III'] = np.where(dfRA['Nível III'] == 'N/I' ,dfRA['Nível III - Financeiro'] ,dfRA['Nível III'])
        dfRA['Nível III'] = np.where(dfRA['Nível III'] == 'N/I' ,dfRA['Nível III - Atendimento'] ,dfRA['Nível III'])
        dfRA['Nível III'] = np.where(dfRA['Nível III'] == 'N/I' ,dfRA['Nível III - Acessórios / Lifestyle / Riders'] ,dfRA['Nível III'])

        #######################################################################

        dfRA['Nível IV'] = np.where(dfRA['Nível IV - Modelo Veículo MINI'] != 'N/I' ,dfRA['Nível IV - Modelo Veículo MINI'] ,dfRA['Nível IV - Modelo Veículo BMW Motorrad'] )
        dfRA['Nível IV'] = np.where(dfRA['Nível IV'] == 'N/I' ,dfRA['Nível IV - Modelo Veículo BMW Brasil'] ,dfRA['Nível IV'])


        dfRA = dfRA.rename(columns={'Nível I' : 'Nível I - Empresa'
                                   ,'Nível II' : 'Nível II - Motivo'
                                   ,'Nível III': 'Nível III - Submotivo'
                                   ,'Nível IV': 'Nível IV - Modelo'
                                     })

        dfRA = dfRA[["Id HugMe","Origem","Id Origem","Data Reclamação","Data Reclamação SLA","Status Hugme","Status RA","Arquivado ?","Congelado?",
                    #"Título","Texto da Reclamação",
                    "Data Avaliacao","Motivo da Reclamação RA","Sentimento RA*","Nome","RG","CPF/CNPJ","Pessoa Física ou Jurídica?","Email","Telefones",
                    "Quantidade de Tags","Tags",
                    #"Nível I - Empresa","Nível II - Motivos",
                    #"Nível III - Acessórios / Lifestyle / Riders","Nível III - Atendimento","Nível III - Financeiro","Nível III - Institucional","Nível III - Peças","Nível III - Processo de Compra",
                    #"Nível III - Produto","Nível III - Recall","Nível III - Serviços","Nível III - Tecnologia","Nível IV - Modelo Veículo BMW Brasil",
                    #"Nível IV - Modelo Veículo BMW Motorrad","Nível IV - Modelo Veículo MINI",
                    "Nível I - Empresa","Nível II - Motivo","Nível III - Submotivo","Nível IV - Modelo",
                    "RA Prime","Região","Resposta da empresa",
                    "Data de Resposta","Data de Resposta SLA","Interações neste ticket","Réplicas na reclamação RA","Seu problema foi resolvido?","Voltaria a fazer negócio?","Nota","Consideração Consumidor","Data Consideração Consumidor","Consideração Empresa",
                    "Data Consideração Empresa","Tempo primeira resposta (privado)","Tempo primeira resposta (público)","Tempo Avaliação",
                    #"Comentários na reclamação*",
                    "Atribuido Para","Quantidade de Atribuições","Redistribuições","Moderações neste ticket","Mensagens internas neste ticket",
                    "Quantidade de lembretes","Data última réplica","Data da última modificação","Avaliacao Favoravel ","Origem RA","Data de Desativação RA","Motivo de Desativação RA","Categorias - FaleConosco","Avaliações desconsideradas RA","Blackfriday RA",
                    "Sentimento",
                    #"Dados Complementares Consumidor",
                    "Avaliado sem resposta RA","Moderação status","Moderação motivo","Moderação data de solicitação","Moderação usuário que solicitou","Moderação data da resposta","Tipo Hugme","Data fechamento",
                    "Quantidade interações consumidor","Quantidade interações empresa",
                    #"Feed tipo",
                    "Fonte informação tipo","Estado","Cidade","data","intervalo","semana","ano",
                    #"num_mes",
                    "nome_mes","dia_semana","dias_reclamacao_resposta","dias_reclamacao_desconsiderados","sla_tempo_resposta","tipo_base","registros","nome_arquivo"]]

        RA = dfRA.drop_duplicates(keep='last')
        RA.index = pd.RangeIndex(len(RA.index))
        del[[dfSLA,dfDesativados,dfRA]]
        return RA


if __name__ == "__main__":

    RA = MergeReclameAqui.mergeRA()