import pandas as pd
import os

##################################################################
##CONFIGURACION DE DIRECTORIOS#######################################################
##################################################################

directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_entrada = os.path.join(directorio_actual, "data(raw)")

ruta_csv_customers = os.path.join(ruta_entrada, "customers.csv")
ruta_csv_sessions = os.path.join(ruta_entrada, "sessions.csv")
ruta_csv_subs = os.path.join(ruta_entrada, "subscription.csv")

ruta_salida = os.path.join(directorio_actual, "data_output")
if not os.path.exists(ruta_salida):
    os.makedirs(ruta_salida)

ruta_salida_customers = os.path.join(ruta_salida, 'customers_limpio.csv')
ruta_salida_sessions = os.path.join(ruta_salida, 'sessions_limpio.csv')
ruta_salida_subs = os.path.join(ruta_salida, 'subs_limpio.csv')

customers=pd.read_csv(ruta_csv_customers, sep=',')
sessions=pd.read_csv(ruta_csv_sessions ,sep=',')
subs=pd.read_csv(ruta_csv_subs, sep=',')


##################################################################
##CUSTOMERS#######################################################
##################################################################
if 'name' in customers.columns:
    print("existe")

# Convierte el nombre a mayúsculas y elimina espacios al inicio y final
customers['name'] = customers['name'].str.upper().str.strip()
customers['customer_id'] = customers['customer_id'].str.upper().str.strip()
customers['plan'] = customers['plan'].str.strip()
customers['segment'] = customers['segment'].str.strip().str.capitalize()


#Limpieza previa de espacios (importante)
customers['signup_date'] = customers['signup_date'].astype(str).str.strip()


customers['signup_date'] = pd.to_datetime(
    customers['signup_date'], 
    dayfirst=True, 
    format='mixed', 
    errors='coerce'
)
customers = customers.drop_duplicates(subset=['customer_id'])




##################################################################
##SESSIONS#######################################################
##################################################################

#Eliminación de duplicados
sessions=sessions.drop_duplicates()

#Inputación de valores con mediana
sessions['sessions'] = sessions['sessions'].fillna(sessions['sessions'].median())
sessions['customer_id'] = sessions['customer_id'].str.strip()

#Formato de fechas
sessions['event_date'] = pd.to_datetime(
    sessions['event_date'], 
    format='mixed',
    errors='coerce')
sessions=sessions.dropna(subset=['event_date'])

#Filtro para exceso de horas mayor a 24 horas
sessions=sessions[sessions['usage_minutes'] <= 1440]



##################################################################
##SUBSCRIPTIONS###################################################
##################################################################
subs['sub_id']=subs['sub_id'].str.strip()
subs['customer_id']=subs['customer_id'].str.strip()

subs['status']=subs['status'].str.strip().str.capitalize()
subs = pd.merge(subs, customers[['customer_id', 'plan']], on='customer_id', how='left')
precios = {
    'PREMIUM': 99.99,
    'BASIC': 29.99,
    'FREE': 0.00
}
subs['amount'] = subs['amount'].fillna(
    subs['plan'].str.upper().str.strip().map(precios)
)
subs=subs.drop(columns=['plan'])

print(customers)
print(sessions)
print(subs)


customers.to_csv(ruta_salida_customers, index=False)
sessions.to_csv(ruta_salida_sessions, index=False)
subs.to_csv(ruta_salida_subs, index=False)

print(f"Archivos limpios guardados en: {directorio_actual}")
