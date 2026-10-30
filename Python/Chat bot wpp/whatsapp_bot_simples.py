"""
WhatsApp Web Bot - Versão Simplificada e Robusta
Autor: ChatBot Assistant
Data: 19/09/2025

Este bot monitora o WhatsApp Web e responde automaticamente
com "aguarde que em breve irei atender" para novas mensagens.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import os
import tempfile

class WhatsAppBotSimples:
    def __init__(self):
        """Inicializa o bot do WhatsApp"""
        self.driver = None
        self.wait = None
        self.mensagem_resposta = "aguarde que em breve irei atender"
        
        # Configura logging mais simples
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def inicializar_chrome(self):
        """Configura e inicializa o Chrome de forma robusta"""
        try:
            print("Inicializando Chrome...")
            
            # Configurações simples do Chrome
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--remote-debugging-port=9222")
            
            # Instala e configura o ChromeDriver automaticamente
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 30)
            
            print("Chrome iniciado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao inicializar Chrome: {e}")
            return False
    
    def fazer_login_whatsapp(self):
        """Faz login no WhatsApp Web"""
        try:
            print("Abrindo WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            
            print("Aguardando página carregar...")
            time.sleep(5)
            
            # Verifica se há QR Code (precisa fazer login)
            try:
                qr_code = self.driver.find_element(By.XPATH, "//canvas[@aria-label='Scan me!']")
                if qr_code:
                    print("🔍 QR CODE DETECTADO!")
                    print("📱 Abra o WhatsApp no seu celular")
                    print("📷 Vá em Configurações > Aparelhos conectados")
                    print("🔗 Clique em 'Conectar um aparelho'")
                    print("📸 Escaneie o QR Code que aparece na tela")
                    print("⏳ Aguardando login...")
                    
                    # Aguarda o QR Code desaparecer (login realizado)
                    contador = 0
                    while True:
                        try:
                            self.driver.find_element(By.XPATH, "//canvas[@aria-label='Scan me!']")
                            time.sleep(2)
                            contador += 1
                            if contador > 60:  # 2 minutos de timeout
                                print("❌ Timeout: Login não realizado em 2 minutos")
                                return False
                        except:
                            print("✅ Login realizado com sucesso!")
                            break
            except:
                print("✅ Já estava logado no WhatsApp Web")
            
            # Aguarda a interface principal carregar
            print("Aguardando interface carregar...")
            time.sleep(10)
            
            # Verifica se conseguiu carregar a lista de conversas
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='pane-side']"))
                )
                print("✅ WhatsApp Web carregado com sucesso!")
                return True
            except:
                print("❌ Interface não carregou corretamente")
                return False
            
        except Exception as e:
            print(f"❌ Erro ao fazer login: {e}")
            return False
    
    def buscar_conversas_nao_lidas(self):
        """Busca conversas com mensagens não lidas"""
        try:
            # Método 1: Busca por badge de contador
            conversas = self.driver.find_elements(
                By.XPATH, 
                "//div[@data-testid='cell-frame-container']//span[@data-testid='icon-unread-count']/../.."
            )
            
            if not conversas:
                # Método 2: Busca por conversas em negrito (alternativa)
                conversas = self.driver.find_elements(
                    By.XPATH,
                    "//div[@data-testid='cell-frame-container'][.//div[contains(@class, 'font-weight-500')]]"
                )
            
            if not conversas:
                # Método 3: Busca mais genérica
                conversas = self.driver.find_elements(
                    By.XPATH,
                    "//div[@data-testid='cell-frame-container']"
                )
                # Filtra apenas as 3 primeiras (mais prováveis de ter mensagens não lidas)
                conversas = conversas[:3] if conversas else []
            
            print(f"📨 Encontradas {len(conversas)} conversas para verificar")
            return conversas
            
        except Exception as e:
            print(f"❌ Erro ao buscar conversas: {e}")
            return []
    
    def enviar_mensagem(self, conversa):
        """Envia mensagem automática"""
        try:
            # Clica na conversa
            conversa.click()
            time.sleep(3)
            
            # Busca a caixa de texto
            caixa_texto = None
            selectors = [
                "//div[@data-testid='conversation-compose-box-input']",
                "//div[@contenteditable='true'][@data-tab='10']",
                "//div[@contenteditable='true'][contains(@class, 'selectable-text')]"
            ]
            
            for selector in selectors:
                try:
                    caixa_texto = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not caixa_texto:
                print("❌ Não foi possível encontrar a caixa de texto")
                return False
            
            # Clica na caixa e digita a mensagem
            caixa_texto.click()
            time.sleep(1)
            caixa_texto.send_keys(self.mensagem_resposta)
            time.sleep(1)
            
            # Envia a mensagem
            caixa_texto.send_keys(Keys.ENTER)
            time.sleep(2)
            
            print("✅ Mensagem enviada com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
            return False
    
    def monitorar_mensagens(self):
        """Monitora mensagens continuamente"""
        print("🤖 Iniciando monitoramento de mensagens...")
        print("💬 Aguardando novas mensagens...")
        print("🛑 Pressione Ctrl+C para parar o bot")
        print("-" * 50)
        
        conversas_processadas = set()
        
        while True:
            try:
                # Busca conversas não lidas
                conversas = self.buscar_conversas_nao_lidas()
                
                for i, conversa in enumerate(conversas):
                    try:
                        # Obtém texto da conversa para identificar
                        texto_conversa = conversa.text
                        identificador = f"{i}_{hash(texto_conversa[:50])}"
                        
                        # Verifica se já processou esta conversa
                        if identificador not in conversas_processadas:
                            print(f"📨 Nova conversa detectada: {identificador}")
                            
                            # Tenta enviar resposta
                            if self.enviar_mensagem(conversa):
                                conversas_processadas.add(identificador)
                                print(f"✅ Resposta enviada para conversa {identificador}")
                            else:
                                print(f"❌ Falha ao enviar resposta para conversa {identificador}")
                            
                            time.sleep(3)  # Pausa entre mensagens
                    
                    except Exception as e:
                        print(f"❌ Erro ao processar conversa {i}: {e}")
                        continue
                
                # Pausa antes da próxima verificação
                print("⏳ Aguardando novas mensagens...")
                time.sleep(10)
                
            except KeyboardInterrupt:
                print("\n🛑 Bot interrompido pelo usuário")
                break
            except Exception as e:
                print(f"❌ Erro no monitoramento: {e}")
                print("🔄 Tentando novamente em 10 segundos...")
                time.sleep(10)
    
    def iniciar(self):
        """Inicia o bot"""
        try:
            print("🤖 WHATSAPP BOT - RESPOSTA AUTOMÁTICA")
            print("=" * 50)
            print("📋 INSTRUÇÕES:")
            print("1. O Chrome será aberto automaticamente")
            print("2. Se aparecer QR Code, escaneie com seu WhatsApp")
            print("3. O bot começará a monitorar automaticamente")
            print("4. Mensagem de resposta: '" + self.mensagem_resposta + "'")
            print("5. Pressione Ctrl+C para parar")
            print("=" * 50)
            
            input("▶️  Pressione Enter para continuar...")
            
            # Inicia Chrome
            if not self.inicializar_chrome():
                print("❌ Falha ao inicializar Chrome")
                return
            
            # Faz login no WhatsApp
            if not self.fazer_login_whatsapp():
                print("❌ Falha ao fazer login no WhatsApp")
                return
            
            # Inicia monitoramento
            self.monitorar_mensagens()
            
        except Exception as e:
            print(f"❌ Erro geral: {e}")
        finally:
            self.fechar()
    
    def fechar(self):
        """Fecha o bot"""
        if self.driver:
            print("🔒 Fechando bot...")
            try:
                self.driver.quit()
            except:
                pass
            print("✅ Bot fechado!")

def main():
    """Função principal"""
    bot = WhatsAppBotSimples()
    bot.iniciar()

if __name__ == "__main__":
    main()