import pandas as pd
import re, os
import numpy as np
import time
from datetime import date, datetime, timedelta



class PastasGenericas:
    ptBRASTEMP = '//acsfs/deptos/CPC/4 - MIS/2 - Cliente/36 - ReclameAqui/04 - Whirlpool/Brastemp/'
    ptCOMPRA_CERTA = '//acsfs/deptos/CPC/4 - MIS/2 - Cliente/36 - ReclameAqui/04 - Whirlpool/Compra certa/'
    ptCONSUL = '//acsfs/deptos/CPC/4 - MIS/2 - Cliente/36 - ReclameAqui/04 - Whirlpool/consul/'
    ptKITCHEN = '//acsfs/deptos/CPC/4 - MIS/2 - Cliente/36 - ReclameAqui/04 - Whirlpool/Kitchen/'
    ptRESULTADO_FINAL = '//acsfs/deptos/CPC/4 - MIS/2 - Cliente/4 - Whirlpool/12 - BackOffice - Paliativo/Dashboard Serviços/Reclame Aqui RA/'
    ptOPERACAO = '//acsfs/deptos/CPC/4 - MIS/2 - Cliente/4 - Whirlpool/12 - BackOffice - Paliativo/Dashboard Serviços/'


class ListaGLOBAIS:

    def dfColunaPADRAO():
        vCOL_PADRAO = pd.DataFrame()
        vCOL_PADRAO = pd.DataFrame(data=vCOL_PADRAO,columns=['Id HugMe','Origem','Id Origem','Data Reclamação','Status Hugme','Status RA','Arquivado ?','Congelado?','Data Avaliacao','Motivo da Reclamação RA'
                                                            ,'Sentimento RA*','Nome','RG','CPF/CNPJ','Pessoa Física ou Jurídica?','Email','Telefones','Cidade','Estado','Quantidade de Tags','Resposta da empresa'
                                                            ,'Data de Resposta','Interações neste ticket','Réplicas na reclamação RA','Seu problema foi resolvido?','Voltaria a fazer negócio?','Nota','Consideração Consumidor'
                                                            ,'Data Consideração Consumidor','Consideração Empresa','Data Consideração Empresa','Tempo primeira resposta (privado)','Tempo primeira resposta (público)'
                                                            ,'Tempo Avaliação','Comentários na reclamação*','Atribuido Para','Quantidade de Atribuições','Redistribuições','Moderações neste ticket','Mensagens internas neste ticket'
                                                            ,'Quantidade de lembretes','Data última réplica','Data da última modificação','Avaliacao Favoravel ','Origem RA','Data de Desativação RA','Motivo de Desativação RA'
                                                            ,'Categorias - FaleConosco','Avaliações desconsideradas RA','Blackfriday RA','Sentimento','Avaliado sem resposta RA','Moderação status','Moderação motivo'
                                                            ,'Moderação data de solicitação','Moderação usuário que solicitou','Moderação data da resposta','Tipo Hugme','Data fechamento','Quantidade interações consumidor'
                                                            ,'Quantidade interações empresa','Fonte informação tipo','Área Brastemp','Migrado para','Motivo da reclamação Serviços','Tentativa','BBlend','Área Consul','Área Kitchenaid'
                                                            ,'Campanhas','Categoria do Produto','Célula Superior','Clube do zero','Dificuldade na URA','Dificuldade na URA','Duplicidade','Marca','Motivo da Reclamação Lojas'
                                                            ,'Solicitação do consumidor','Solicitou nota','Solução Final','Solução Inicial','Status garantia','nome_arquivo'])
        return vCOL_PADRAO


    def dfListaMESES():
        dfMESES = [["01","01-JANEIRO"],["02","02-FEVEREIRO"],["03","03-MARÇO"],["04","04-ABRIL"],["05","05-MAIO"],["06","06-JUNHO"],["07","07-JULHO"],["08","08-AGOSTO"],["09","09-SETEMBRO"],["10","10-OUTUBRO"],["11","11-NOVEMBRO"],["12","12-DEZEMBRO"]]

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
        return dfREGIAO


class FuncoesPersonalizadas:

    semana = ['2ª seg','3ª ter','4ª qua','5ª qui','6ª sex','7ª sab','1ª dom']

    def __string__(self, semana):

        self.semana = semana

    def convDT_RECL_ABREV(self,string):
        if string == None or string =='None':
            retorno = None
        else:
            retorno = format(datetime.strptime(string[:10],'%Y-%m-%d').date(),'%Y-%m-%d')
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

    def convINTERVALO(self,string):
        if(string == None):
            retorno = None
        else:
            retorno = (string[11:])[:2]+":00:00"
        return retorno

    def strMAIUSCULA(self,string):
        try:
            retorno = string.upper()
        except:
            retorno = None
        return retorno


class ExcelBases:

    def ReclameAqui():

        p = PastasGenericas
        f = FuncoesPersonalizadas()

        lPASTA = [1]
        vBASES = pd.DataFrame()

        for i in lPASTA:

            vLIST_ARQ = [os.path.join(p.ptBRASTEMP, nome) for nome in os.listdir(p.ptBRASTEMP)]
            vARQ_LIST = [arq for arq in vLIST_ARQ if os.path.isfile(arq)]
            vARQ_TIPO = [arq for arq in vARQ_LIST if arq.lower().endswith(".xlsx")]

            vBRASTEMP = pd.DataFrame()
            for arq in vARQ_TIPO:

                vUPLOAD = pd.read_excel(arq,skiprows = 3) #header=None, skiprows = elimina linhas do df , encoding='latin_1'
                vUPLOAD['nome_arquivo']= 'Brastemp'

                vBRASTEMP = vBRASTEMP.append(vUPLOAD)
            vBASES = vBASES.append(vBRASTEMP)
            del[vUPLOAD]

            #------------------------------------------------------------------------------------------

            vLIST_ARQ = [os.path.join(p.ptCOMPRA_CERTA, nome) for nome in os.listdir(p.ptCOMPRA_CERTA)]
            vARQ_LIST = [arq for arq in vLIST_ARQ if os.path.isfile(arq)]
            vARQ_TIPO = [arq for arq in vARQ_LIST if arq.lower().endswith(".xlsx")]

            vCOMPRA_CERTA = pd.DataFrame()
            for arq in vARQ_TIPO:

                vUPLOAD = pd.read_excel(arq,skiprows = 3) #header=None, skiprows = elimina linhas do df , encoding='latin_1'
                vUPLOAD['nome_arquivo']= 'Compra Certa'

                vCOMPRA_CERTA = vCOMPRA_CERTA.append(vUPLOAD)
            vBASES = vBASES.append(vCOMPRA_CERTA)
            del[vUPLOAD]

            #------------------------------------------------------------------------------------------

            vLIST_ARQ = [os.path.join(p.ptCONSUL, nome) for nome in os.listdir(p.ptCONSUL)]
            vARQ_LIST = [arq for arq in vLIST_ARQ if os.path.isfile(arq)]
            vARQ_TIPO = [arq for arq in vARQ_LIST if arq.lower().endswith(".xlsx")]

            vCONSUL = pd.DataFrame()
            for arq in vARQ_TIPO:

                vUPLOAD = pd.read_excel(arq,skiprows = 3) #header=None, skiprows = elimina linhas do df , encoding='latin_1'
                vUPLOAD['nome_arquivo']= 'Consul'

                vCONSUL = vCONSUL.append(vUPLOAD)
            vBASES = vBASES.append(vCONSUL)
            del[vUPLOAD]

            #------------------------------------------------------------------------------------------

            vLIST_ARQ = [os.path.join(p.ptKITCHEN, nome) for nome in os.listdir(p.ptKITCHEN)]
            vARQ_LIST = [arq for arq in vLIST_ARQ if os.path.isfile(arq)]
            vARQ_TIPO = [arq for arq in vARQ_LIST if arq.lower().endswith(".xlsx")]

            vKITCHEN = pd.DataFrame()
            for arq in vARQ_TIPO:

                vUPLOAD = pd.read_excel(arq,skiprows = 3) #header=None, skiprows = elimina linhas do df , encoding='latin_1'
                vUPLOAD['nome_arquivo']= 'Kitchen'

                vKITCHEN = vKITCHEN.append(vUPLOAD)

            vBASES = vBASES.append(vKITCHEN)
            del[vUPLOAD]

            #------------------------------------------------------------------------------------------
            continue

        del[[vBRASTEMP,vCOMPRA_CERTA,vCONSUL,vKITCHEN]]

        dfMESES = ListaGLOBAIS.dfListaMESES()
        dfMESES = pd.DataFrame(data=dfMESES,columns=['num_mes','nome_mes'])

        dfREGIAO = ListaGLOBAIS.dfListaREGIAO()
        dfREGIAO = pd.DataFrame(data=dfREGIAO,columns=['Estado','Região'])


        #------------------------------------------------------------------------------------------
        #Df Padrão
        vCOL_PADRAO = ListaGLOBAIS.dfColunaPADRAO()

        #Qtd. Colunas importadas df "vCOL_PADRAO"
        COLUNAS_DF = vCOL_PADRAO.columns.values
        vNOME_COLUNA_DF = pd.DataFrame(data=COLUNAS_DF,columns=['nome_coluna']) #transforma coluna em df
        vMAX_INDICE_COL = len(vNOME_COLUNA_DF.index)

        #Qtd. Colunas importadas df "vBASES"
        COLUNAS_DF = vBASES.columns.values
        vNOME_COLUNA_DF = pd.DataFrame(data=COLUNAS_DF,columns=['nome_coluna']) #transforma coluna em df
        vMAX_INDICE_COL_2 = len(vNOME_COLUNA_DF.index)


        #Inclui coluna faltante
        vINICIAL = 0

        while vINICIAL < vMAX_INDICE_COL:
            if (vCOL_PADRAO.columns[vINICIAL] in vBASES.columns)==False: #verifica se coluna existe no DataFrame
                #set(vCOL_PADRAO.columns[0]).issubset(vBASES.columns) == False:
                #print('Coluna Existe: '+vBASES.columns[vINICIAL])
                vBASES['Coluna_Faltante'] = None
                vBASES = vBASES.rename(columns={'Coluna_Faltante': vCOL_PADRAO.columns[vINICIAL]})

            # else:
            #     print('Coluna Existe: '+vCOL_PADRAO.columns[vINICIAL])



            vINICIAL += 1

        #------------------------------------------------------------------------------------------

        #'Título','Texto da Reclamação',
        vBASES = vBASES[['Id HugMe','Origem','Id Origem','Data Reclamação','Status Hugme','Status RA','Arquivado ?','Congelado?','Data Avaliacao','Motivo da Reclamação RA','Sentimento RA*'
                        ,'Nome','RG','CPF/CNPJ','Pessoa Física ou Jurídica?','Email','Telefones','Cidade','Estado','Quantidade de Tags','Resposta da empresa','Data de Resposta'
                        ,'Interações neste ticket','Réplicas na reclamação RA','Seu problema foi resolvido?','Voltaria a fazer negócio?','Nota','Consideração Consumidor','Data Consideração Consumidor'
                        ,'Consideração Empresa','Data Consideração Empresa','Tempo primeira resposta (privado)','Tempo primeira resposta (público)','Tempo Avaliação','Comentários na reclamação*'
                        ,'Atribuido Para','Quantidade de Atribuições','Redistribuições','Moderações neste ticket','Mensagens internas neste ticket','Quantidade de lembretes','Data última réplica'
                        ,'Data da última modificação','Avaliacao Favoravel ','Origem RA','Data de Desativação RA','Motivo de Desativação RA','Categorias - FaleConosco','Avaliações desconsideradas RA'
                        ,'Blackfriday RA','Sentimento','Avaliado sem resposta RA','Moderação status','Moderação motivo','Moderação data de solicitação','Moderação usuário que solicitou'
                        ,'Moderação data da resposta','Tipo Hugme','Data fechamento','Quantidade interações consumidor','Quantidade interações empresa','Fonte informação tipo','Área Brastemp'
                        ,'Migrado para','Motivo da reclamação Serviços','Tentativa','BBlend','Área Consul','Área Kitchenaid','Campanhas','Categoria do Produto','Célula Superior','Clube do zero'
                        ,'Dificuldade na URA','Dificuldade na URA','Duplicidade','Marca','Motivo da Reclamação Lojas','Solicitação do consumidor','Solicitou nota','Solução Final','Solução Inicial'
                        ,'Status garantia','nome_arquivo']]


        vBASES = vBASES[vBASES['Avaliações desconsideradas RA'] == 'não']
        vBASES['num_mes'] = (vBASES['Data Reclamação'].apply(str).apply(f.convMES))
        vBASES = vBASES.merge(dfMESES, how='left', on='num_mes')
        vBASES = vBASES.merge(dfREGIAO, how='left', on='Estado')
        #------------------------------------------------------------------------------------------
        vBASES['Nome'] = (vBASES['Nome'].apply(str).apply(f.strMAIUSCULA))


        #------------------------------------------------------------------------------------------
        vBASES['semana'] = (vBASES['Data Reclamação'].apply(str).apply(f.convSEMANA))
        vBASES['ano'] = (vBASES['Data Reclamação'].apply(str).apply(f.convANO))
        vBASES['intervalo'] = (vBASES['Data Reclamação'].apply(str).apply(f.convINTERVALO))
        vBASES['data_reclamacao'] = (vBASES['Data Reclamação'].apply(str).apply(f.convDT_RECL_ABREV))

        #------------------------------------------------------------------------------------------
        vBASES['Área Brastemp'] = vBASES['Área Brastemp'].replace({pd.NaT: 'Sem Área', np.NaN: 'Sem Área'})
        vBASES['Área Consul'] = vBASES['Área Consul'].replace({pd.NaT: 'Sem Área', np.NaN: 'Sem Área'})
        vBASES['Área Kitchenaid'] = vBASES['Área Kitchenaid'].replace({pd.NaT: 'Sem Área', np.NaN: 'Sem Área'})

        # vBASES['Área'] = np.where(vBASES['Área Brastemp'] != 'Sem Área' ,vBASES['Área Brastemp'] ,'Área Consul')
        # vBASES['Área'] = np.where(vBASES['Área Kitchenaid'] != 'Sem Área' ,vBASES['Área Kitchenaid'] ,vBASES['Área'])

        vBASES['Área'] = np.where(vBASES['Área Brastemp'] != 'Sem Área' ,vBASES['Área Brastemp'] ,vBASES['Área Consul'])
        vBASES['Área'] = np.where(vBASES['Área Consul'] != 'Sem Área' ,vBASES['Área Consul'],vBASES['Área'])
        vBASES['Área'] = np.where(vBASES['Área Kitchenaid'] != 'Sem Área' ,vBASES['Área Kitchenaid'] ,vBASES['Área'])

        #------------------------------------------------------------------------------------------
        vBASES['nome_arquivo'] = vBASES['nome_arquivo'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})

        #------------------------------------------------------------------------------------------
        vBASES['Estado'] = vBASES['Estado'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        vBASES['Cidade'] = vBASES['Cidade'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        vBASES['Região'] = vBASES['Região'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        vBASES['Atribuido Para'] = vBASES['Atribuido Para'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})

        #------------------------------------------------------------------------------------------
        vBASES['Nome'] = vBASES['Nome'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})

        #------------------------------------------------------------------------------------------
        vBASES['Voltaria a fazer negócio?'] = vBASES['Voltaria a fazer negócio?'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        vBASES['Status RA'] = vBASES['Status RA'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})

        #------------------------------------------------------------------------------------------
        vBASES['Motivo da Reclamação Serviços'] = vBASES['Motivo da reclamação Serviços'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        vBASES['Motivo da Reclamação Lojas'] = vBASES['Motivo da Reclamação Lojas'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        vBASES['Categoria do Produto'] = vBASES['Categoria do Produto'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})
        vBASES['Solicitou nota'] = vBASES['Solicitou nota'].replace({pd.NaT: 'N/I', np.NaN: 'N/I'})

        vBASES.drop(['Motivo da reclamação Serviços'], axis=1, inplace=True)

        vBASES['registros'] = 1
        vBASES.index = pd.RangeIndex(len(vBASES.index))



        del[[dfMESES,dfREGIAO]]

        return vBASES


class ModuloGravacao:


    def mdgravacao():

        p = PastasGenericas
        vRA = ExcelBases.ReclameAqui()

        vMES = str((date.today()).month)

        if len(vMES) == 1:
            vMES = '0'+vMES
        else:
            vMES

        vANO = str((date.today()).year)

        vMES_ANO = vRA[['ano','num_mes']]
        vMES_ANO = vMES_ANO.drop_duplicates()
        vMES_ANO = vMES_ANO.sort_values(['ano', 'num_mes']) #ordena
        vMES_ANO.index = pd.RangeIndex(len(vMES_ANO.index))
        vMES_ANO['coluna_id'] = pd.RangeIndex(len(vMES_ANO.index))
        vMES_ANO['importar?'] = np.where(vMES_ANO['ano']+vMES_ANO['num_mes'] == vANO+vMES ,'sim' ,'nao')
        #vMES_ANO['importar?'] = np.where(vMES_ANO['ano']+vMES_ANO['num_mes'] == vANO+vMES ,'sim' ,'sim') #gravação do retroativo substituir por sim

        vMES_ANO
        vIMPORTACAO = vMES_ANO[vMES_ANO['importar?'] =='sim']


        vMAX_ID = vIMPORTACAO['coluna_id'].max()
        vMIN_ID = vIMPORTACAO['coluna_id'].min()


        while vMAX_ID >= vMIN_ID:

            vIMPORTACAO_1 = vIMPORTACAO[vIMPORTACAO['coluna_id'] == vMAX_ID]
            vANO_I = vIMPORTACAO_1.iloc[0,0]
            vMES_I = vIMPORTACAO_1.iloc[0,1]

            vSAVE = vRA[vRA['ano'] == vANO_I]
            vSAVE = vSAVE[vSAVE['num_mes'] == vMES_I]
            vSAVE.to_csv(p.ptRESULTADO_FINAL+'RA_Whirlpool_'+vMES_I+'_'+vANO_I+'.csv', index=False,sep = ';', line_terminator='\n') #,encoding='latin_1' or utf-8"

            vMAX_ID -= 1

        return vRA



if __name__ == "__main__":

    RA = ModuloGravacao.mdgravacao()