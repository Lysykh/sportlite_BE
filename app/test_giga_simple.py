# test_giga_simple.py
import ssl
from gigachat import GigaChat

def main():
    print("Тестирую GigaChat напрямую...")
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        giga = GigaChat(
            credentials='MWIwYjY4ZjctYmQ1Ny00MDcyLWEzNWMtYzYwNWY4NTNjNjg5OmJmOWI3YmYyLThmNDAtNDFhMi05ZGI2LTI0ZmVmMTY4ZDY5MA==',
            verify_ssl_certs=False,
            ssl_context=ssl_context,
            timeout=10
        )
        
        response = giga.chat("Привет")
        print(f"✅ Успех: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()