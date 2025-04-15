"""
Módulo que permite interactuar con la API de OpenAI.
El usuario ingresa consultas por consola, y se imprime la respuesta de chatGPT.
Incluye manejo de errores, historial de consultas y formato de salida.
"""

import os
import pyreadline as readline

import openai
from dotenv import load_dotenv

# Cargar la clave API desde variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Crear cliente
client = openai.OpenAI()

# Contexto del sistema para la conversación
CONTEXT = "Sos un asistente útil que responde preguntas del usuario."
USERTASK = "Responder la siguiente pregunta del usuario."

# Almacena la última consulta del usuario
ULTIMA_CONSULTA = ""


def main():
    """Bucle principal para leer, enviar y mostrar respuestas de la API."""
    global ULTIMA_CONSULTA
    while True:
        print("\n--- Nueva consulta (Ctrl+C para salir) ---")

        try:
            if ULTIMA_CONSULTA:
                readline.add_history(ULTIMA_CONSULTA)

            user_query = input("Ingresá tu consulta: ").strip()

            try:
                if not user_query:
                    raise ValueError("La consulta no puede estar vacía.")

                print(f"\nYou: {user_query}")
                ULTIMA_CONSULTA = user_query

                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini-2024-07-18",
                        response_format={"type": "json_object"},
                        messages=[
                            {"role": "system", "content": CONTEXT},
                            {"role": "user", "content": USERTASK},
                            {"role": "user", "content": user_query}
                        ],
                        temperature=1,
                        max_tokens=1024,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )

                    print(f"\nchatGPT: {response.choices[0].message.content}")

                except openai.APIError as api_error:
                    print("Error en la API:", api_error)

            except ValueError as value_error:
                print("Error de validación:", value_error)

        except KeyboardInterrupt:
            print("\nPrograma terminado por el usuario.")
            break


if __name__ == "__main__":
    main()
