import pandas as pd
import re, os

class PastasGenericas:
    ptBRASTEMP = '//acsfs/deptos/CPC/4 - MIS/2 - Cliente/36 - ReclameAqui/04 - Whirlpool/Regua Planejado/'

class Planejado:

    def BasePlanejado():

        p = PastasGenericas

        lPASTA = [1]
        vBASES = pd.DataFrame()

        for i in lPASTA:

            vLISTA = [os.path.join(p.ptBRASTEMP, nome) for nome in os.listdir(p.ptBRASTEMP)]
            vARQUIVO = [arq for arq in vLISTA if os.path.isfile(arq)]
            vXLSX = [arq for arq in vARQUIVO if arq.lower().endswith(".xlsx")]

            arqRECLAME_AQUI = pd.DataFrame()
            for arq in vXLSX:
                arquivo_csv = pd.read_excel(arq, sheet_name='RECLAME AQUI') #encoding='latin_1', skiprows=3
                arqRECLAME_AQUI = arqRECLAME_AQUI.append(arquivo_csv)
                arqRECLAME_AQUI['nome_arquivo'] ='RECLAME AQUI'
            vBASES = vBASES.append(arqRECLAME_AQUI)

        #------------------------------------------------------------------------------------------

            vLISTA = [os.path.join(p.ptBRASTEMP, nome) for nome in os.listdir(p.ptBRASTEMP)]
            vARQUIVO = [arq for arq in vLISTA if os.path.isfile(arq)]
            vXLSX = [arq for arq in vARQUIVO if arq.lower().endswith(".xlsx")]

            arqCONSUMIDOR_GOV = pd.DataFrame()
            for arq in vXLSX:
                arquivo_csv = pd.read_excel(arq, sheet_name='CONSUMIDOR GOV') #encoding='latin_1', skiprows=3
                arqCONSUMIDOR_GOV = arqCONSUMIDOR_GOV.append(arquivo_csv)
                arqCONSUMIDOR_GOV['nome_arquivo'] ='CONSUMIDOR GOV'
            vBASES = vBASES.append(arqCONSUMIDOR_GOV)


            continue

        del[[arqRECLAME_AQUI,arqCONSUMIDOR_GOV]]


        return vBASES


if __name__ == "__main__":

    PLANEJADO = Planejado.BasePlanejado()