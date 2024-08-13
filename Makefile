run:
# Ejecuta el programa
	streamlit run main.py

cred:
# Ejecuta el programa
	@py -c "from my_secrets.generate_keys import crear_credenciales; crear_credenciales()";