import psycopg2
import pandas as pd
import pandas.io.sql as psql


class PastasGenericas:
    ptOPERACAO = '//acsfs/deptos/CPC/4 - MIS/2 - Cliente/4 - Whirlpool/12 - BackOffice - Paliativo/Dashboard Serviços/'

class ListasGenericas:

    def lista_OPERACAO():
        p = PastasGenericas
        arqOPERACAO = pd.read_excel(p.ptOPERACAO+'DE PARA NOME OPERACAO.xlsx', sheet_name='OPERACAO') #encoding='latin_1'
        arqOPERACAO = arqOPERACAO[arqOPERACAO['TIPO_DOC']=='REC']
        arqOPERACAO = arqOPERACAO[arqOPERACAO['CONSIDERAR']!='-']
        arqOPERACAO = arqOPERACAO[['FILA']]
        arqOPERACAO.index = pd.RangeIndex(len(arqOPERACAO.index)) #indexar novamente
        arqOPERACAO = str(arqOPERACAO.values.tolist()).replace('[','').replace(']','')
        return arqOPERACAO

class ConnPostgreSQL:

    def querySQL():
        conn = psycopg2.connect(host='10.200.50.12'
                               ,database='Backoffice_Service'
                               ,user='usr_dvlpowerbi'
                               ,password='algar@2020')
        return conn

class Querysql:

    def qyBACKLOG():
        qyery_backlog = ("select "
                        " to_date(cb.dt_processamento,'yyyy-mm-dd') as dt_processamento"
                        ",cb.celula_final "
                        ",cb.filas"
                        ",sum(registro_geral) as registro_geral"
                        ",sum(registro_atraso) as registro_atraso"
                        " from("
                        "SELECT"
                        " dt_processamento"
                        ",celula_final "
                        ",filas"
                        ",fup_flague_atraso"
                        ",1 as registro_geral"
                        ",case when fup_flague_atraso='1 - ATRASADO' then 1 else 0 end registro_atraso"
                        " FROM bases_services.base_crm"
                        " where  filas in ('RA - Reclamação','GOV - Reclamação')"
                        " and filas in ('RA - Reclamação','GOV - Reclamação')"
                        ")cb where cb.celula_final in ('Consumidor.Gov','Reclame Aqui') group by cb.dt_processamento,cb.celula_final,cb.filas")
                        #" fetch first 10 rows only")
        return qyery_backlog

    def qyDIAS():

        l = ListasGenericas
        arqOPERACAO = l.lista_OPERACAO()

        query_20_30_dias = ("select "
                            " cb.dt_processamento"
                            " ,cb.celula_final"
                            " ,sum(cb.qtde_doc_pendente) as qtde_doc_pendente"
                            " ,sum(cb.pendente_20_dias) as pendente_20_dias"
                            " ,sum(cb.pendente_30_dias) as pendente_30_dias"
                            " from("
                            " SELECT "
                            "  to_date(concat(right(p.dt_processamento,4),'-',right(left(p.dt_processamento,5),2),'-',left(p.dt_processamento,2)),'yyyy-mm-dd') as dt_processamento"
                            " ,p.tipo_doc"
                            " ,aux_0.celula_final"
                            " ,p.filas"
                            " ,p.aging_dt_primeiro_envio"
                            " ,p.qtde_doc_pendente"
                            " ,case when p.aging_dt_primeiro_envio<=20 then 1 else 0 end pendente_20_dias"
                            " ,case when p.aging_dt_primeiro_envio<=30 then 1 else 0 end pendente_30_dias"
                            " FROM bases_services.fato_pendente p"
                            " left join ("
                            " select distinct celula_final, filas"
                            " FROM bases_services.base_crm"
                            " where celula_final in ('Consumidor.Gov','Reclame Aqui')"
                            " ) aux_0 on (aux_0.filas = p.filas)"
                            " where p.tipo_doc='REC'"
                            " and p.filas in ({vOPERACAO})"
                            " )cb "
                            " where cb.celula_final in ('Consumidor.Gov','Reclame Aqui')"
                            " group by cb.dt_processamento ,cb.celula_final".format(vOPERACAO=arqOPERACAO))
        return query_20_30_dias


class ConsultaSQL:

    def dadosSQL():
        q = Querysql

        qyery_backlog = q.qyBACKLOG()
        query_20_30_dias = q.qyDIAS()

        c = ConnPostgreSQL
        conn = c.querySQL()

        dfBACKLOG_1 = psql.read_sql(qyery_backlog, conn)
        dfDIAS_0 = psql.read_sql(query_20_30_dias, conn)


        dfBACKLOG_1['qtde_doc_pendente'] = None
        dfBACKLOG_1['pendente_20_dias'] = None
        dfBACKLOG_1['pendente_30_dias'] = None
        dfBACKLOG_1['base']='PENDENTE BACKLOG'


        dfDIAS_0['filas'] = ''
        dfDIAS_0['registro_geral'] = None
        dfDIAS_0['registro_atraso'] = None
        dfDIAS_0['base']='PENDENTE 20 E 30 DIAS'


        dfPENDENTE = pd.concat([dfBACKLOG_1,dfDIAS_0])
        dfPENDENTE = dfPENDENTE[['dt_processamento','celula_final','filas','registro_geral','registro_atraso','qtde_doc_pendente','pendente_20_dias','pendente_30_dias','base']]

        return dfPENDENTE

if __name__ == "__main__":
    #p = PastasGenericas
    PENDENTE = ConsultaSQL.dadosSQL()