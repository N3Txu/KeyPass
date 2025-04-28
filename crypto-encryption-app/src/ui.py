import sys

class UserInterface:
    def __init__(self):
        self.message = ""
        self.algorithm = "Caesar"
        self.key = ""

    def display_main_menu(self):
        # Menú principal de la aplicación
        print("\nAplicación de Criptografía")
        print("1. Cifrar un mensaje")
        print("2. Descifrar un mensaje")
        print("3. Salir")
        choice = input("Ingrese su opción: ")
        return choice

    def get_message_input(self):
        return input("Ingrese su mensaje: ")

    def select_algorithm(self):
        print("\nSeleccione el algoritmo de cifrado:")
        print("1. César")
        print("2. AES")
        print("3. RSA")
        print("4. Híbrido")
        choice = input("Ingrese su opción: ")
        if choice == "1":
            self.algorithm = "caesar"
            return "caesar"
        elif choice == "2":
            self.algorithm = "aes"
            return "aes"
        elif choice == "3":
            self.algorithm = "rsa"
            return "rsa"
        elif choice == "4":
            self.algorithm = "hybrid"
            return "hybrid"
        else:
            print("Opción inválida. Predeterminado a César.")
            self.algorithm = "caesar"
            return "caesar"

    def get_key_input(self):
        if self.algorithm == "hybrid":
            return ""
        return input("Ingrese su clave: ")

    def get_encrypted_message_input(self):
        return input("Ingrese su mensaje cifrado: ")

    def display_result(self, result):
        print("\nResultado:")
        print(result)

    def display_invalid_choice_message(self):
        print("Opción inválida. Por favor, intente de nuevo.")

    def display_exit_message(self):
        print("Saliendo de la aplicación. ¡Adiós!")

    # Nota: un método run() separado está en desuso; use el bucle main.py para la ejecución

if __name__ == "__main__":
    ui = UserInterface()
    # Ejemplo de ejecución independiente (no se usa en main.py integrado)
    choice = ui.display_main_menu()
    print(f"Seleccionado {choice}")