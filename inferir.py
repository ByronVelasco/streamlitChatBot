import joblib

# Datos fijos para prueba
features = [[5.1, 3.5, 1.4, 0.2]]
# Cargar el modelo
modelo = joblib.load("model.pkl")
# Hacer la predicción
prediccion = modelo.predict(features)
print("Predicción:", prediccion[0])
