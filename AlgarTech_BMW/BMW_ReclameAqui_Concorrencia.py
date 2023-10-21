import pandas as pd
import os
import re

class PastasGenericas:

    vLIST_PASTAS = '//acsfs/DEPTOS/CPC/4 - MIS/2 - Cliente/36 - ReclameAqui/01 - BMW/Concorrencia/'

class Concorrencia:

    def ConcorrenciaRA():

        p = PastasGenericas

        vLISTA = [os.path.join(p.vLIST_PASTAS, nome) for nome in os.listdir(p.vLIST_PASTAS)]
        dfConcorrencia = pd.DataFrame()
        for h in vLISTA:

            if str(re.findall(r'Concorrencia.*',h)).replace(r'Concorrencia/','').replace("['",'').replace("']",'') == 'Carro':

                vLISTA = [os.path.join(p.vLIST_PASTAS+'Carro/', nome) for nome in os.listdir(p.vLIST_PASTAS+'Carro/')]
                vlist_arquivo = [arq for arq in vLISTA if os.path.isfile(arq)]
                vlist_xls = [arq for arq in vlist_arquivo if arq.lower().endswith(".xlsx")]
                dfConcorrencia_1 = pd.DataFrame()

                for arq in vlist_xls:
                    arquivo_csv = pd.read_excel(arq, encoding='latin_1')
                    dfConcorrencia_1 = dfConcorrencia_1.append(arquivo_csv)
                dfConcorrencia_1['arquivo_origem'] = 'Concorrencia Carro'
                dfConcorrencia = dfConcorrencia.append(dfConcorrencia_1)

            elif str(re.findall(r'Concorrencia.*',h)).replace(r'Concorrencia/','').replace("['",'').replace("']",'')   == 'Moto':

                vLISTA = [os.path.join(p.vLIST_PASTAS+'Moto/', nome) for nome in os.listdir(p.vLIST_PASTAS+'Moto/')]
                vlist_arquivo = [arq for arq in vLISTA if os.path.isfile(arq)]
                vlist_xls = [arq for arq in vlist_arquivo if arq.lower().endswith(".xlsx")]
                dfConcorrencia_2 = pd.DataFrame()

                for arq in vlist_xls:
                    arquivo_csv = pd.read_excel(arq, encoding='latin_1')
                    dfConcorrencia_2 = dfConcorrencia_2.append(arquivo_csv)
                dfConcorrencia_2['arquivo_origem'] = 'Concorrencia Moto'
                dfConcorrencia = dfConcorrencia.append(dfConcorrencia_2)

            continue

        dfConcorrencia.index = pd.RangeIndex(len(dfConcorrencia.index))
        Concorrencia = dfConcorrencia

        del [[arquivo_csv ,dfConcorrencia ,dfConcorrencia_1,dfConcorrencia_2]]

        return Concorrencia


if __name__ == "__main__":

    Concorrencia = Concorrencia.ConcorrenciaRA()