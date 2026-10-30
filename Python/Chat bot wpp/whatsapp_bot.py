"""
WhatsApp Web Bot - Resposta Automática
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

class WhatsAppBot:
    def __init__(self):
        """Inicializa o bot do WhatsApp"""
        self.driver = None
        self.wait = None
        self.mensagem_resposta = "aguarde que em breve irei atender"
        self.conversas_respondidas = set()  # Controla quais conversas já foram respondidas
        
        # Configura logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('whatsapp_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def inicializar_driver(self):
        """Configura e inicializa o driver do Chrome"""
        try:
            self.logger.info("Inicializando driver do Chrome...")
            
            # Configurações do Chrome
            options = webdriver.ChromeOptions()
            # Cria diretório temporário único para dados do usuário
            temp_dir = os.path.join(tempfile.gettempdir(), f"chrome_data_{int(time.time())}")
            options.add_argument(f"--user-data-dir={temp_dir}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Instala e configura o ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 20)
            
            self.logger.info("Driver iniciado com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao inicializar driver: {e}")
            return False
    
    def abrir_whatsapp_web(self):
        """Abre o WhatsApp Web no navegador"""
        try:
            self.logger.info("Abrindo WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            
            # Aguarda a página carregar completamente
            self.logger.info("Aguardando página carregar...")
            time.sleep(5)
            
            # Verifica se precisa fazer login (QR Code)
            try:
                qr_code = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Scan me!']"))
                )
                self.logger.info("QR Code detectado! Escaneie com seu celular para fazer login.")
                self.logger.info("Aguardando login...")
                
                # Aguarda até o QR Code desaparecer (login realizado)
                self.wait.until(
                    EC.invisibility_of_element_located((By.XPATH, "//canvas[@aria-label='Scan me!']"))
                )
                self.logger.info("Login realizado com sucesso!")
                
            except:
                self.logger.info("Já está logado no WhatsApp Web")
            
            # Aguarda a interface principal carregar
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='pane-side']"))
            )
            self.logger.info("WhatsApp Web carregado com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao abrir WhatsApp Web: {e}")
            return False
    
    def obter_conversas_nao_lidas(self):
        """Obtém lista de conversas com mensagens não lidas"""
        try:
            # Procura por conversas com badge de mensagens não lidas
            conversas_nao_lidas = self.driver.find_elements(
                By.XPATH, 
                "//div[@data-testid='cell-frame-container']//span[@data-testid='icon-unread-count']/.."
            )
            
            if not conversas_nao_lidas:
                # Alternativa: procura por conversas em negrito (não lidas)
                conversas_nao_lidas = self.driver.find_elements(
                    By.XPATH,
                    "//div[@data-testid='cell-frame-container'][.//span[contains(@class, 'font-weight')]]"
                )
            
            self.logger.info(f"Encontradas {len(conversas_nao_lidas)} conversas não lidas")
            return conversas_nao_lidas
            
        except Exception as e:
            self.logger.error(f"Erro ao obter conversas não lidas: {e}")
            return []
    
    def obter_nome_conversa(self, conversa_element):
        """Obtém o nome da conversa"""
        try:
            nome_element = conversa_element.find_element(
                By.XPATH, 
                ".//span[@data-testid='conversation-info-header']"
            )
            return nome_element.text
        except:
            try:
                # Alternativa para obter nome
                nome_element = conversa_element.find_element(
                    By.XPATH,
                    ".//span[@title]"
                )
                return nome_element.get_attribute("title")
            except:
                return "Conversa desconhecida"
    
    def enviar_resposta_automatica(self, conversa_element):
        """Envia resposta automática para uma conversa"""
        try:
            # Clica na conversa
            conversa_element.click()
            time.sleep(2)
            
            # Procura pela caixa de texto
            caixa_texto = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@data-testid='conversation-compose-box-input']")
                )
            )
            
            # Digita a mensagem
            caixa_texto.click()
            caixa_texto.send_keys(self.mensagem_resposta)
            
            # Envia a mensagem (Enter)
            caixa_texto.send_keys(Keys.ENTER)
            
            self.logger.info("Resposta automática enviada com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar resposta automática: {e}")
            return False
    
    def monitorar_mensagens(self):
        """Monitora continuamente por novas mensagens"""
        self.logger.info("Iniciando monitoramento de mensagens...")
        
        while True:
            try:
                # Obtém conversas não lidas
                conversas_nao_lidas = self.obter_conversas_nao_lidas()
                
                for conversa in conversas_nao_lidas:
                    try:
                        nome_conversa = self.obter_nome_conversa(conversa)
                        
                        # Verifica se já respondeu a esta conversa
                        if nome_conversa not in self.conversas_respondidas:
                            self.logger.info(f"Nova mensagem de: {nome_conversa}")
                            
                            # Envia resposta automática
                            if self.enviar_resposta_automatica(conversa):
                                self.conversas_respondidas.add(nome_conversa)
                                self.logger.info(f"Resposta enviada para: {nome_conversa}")
                            
                            time.sleep(2)  # Pausa entre respostas
                    
                    except Exception as e:
                        self.logger.error(f"Erro ao processar conversa: {e}")
                        continue
                
                # Aguarda antes de verificar novamente
                time.sleep(5)
                
            except KeyboardInterrupt:
                self.logger.info("Bot interrompido pelo usuário")
                break
            except Exception as e:
                self.logger.error(f"Erro no monitoramento: {e}")
                time.sleep(10)  # Pausa maior em caso de erro
    
    def iniciar_bot(self):
        """Inicia o bot do WhatsApp"""
        try:
            self.logger.info("=== INICIANDO WHATSAPP BOT ===")
            
            # Inicializa driver
            if not self.inicializar_driver():
                return False
            
            # Abre WhatsApp Web
            if not self.abrir_whatsapp_web():
                return False
            
            # Inicia monitoramento
            self.monitorar_mensagens()
            
        except Exception as e:
            self.logger.error(f"Erro geral do bot: {e}")
        finally:
            self.fechar_bot()
    
    def fechar_bot(self):
        """Fecha o bot e limpa recursos"""
        if self.driver:
            self.logger.info("Fechando bot...")
            self.driver.quit()
            self.logger.info("Bot fechado com sucesso!")

def main():
    """Função principal"""
    bot = WhatsAppBot()
    
    print("=== WHATSAPP BOT - RESPOSTA AUTOMÁTICA ===")
    print("Este bot irá responder automaticamente às mensagens recebidas")
    print("com: 'aguarde que em breve irei atender'")
    print()
    print("INSTRUÇÕES:")
    print("1. O Chrome será aberto automaticamente")
    print("2. Se solicitado, escaneie o QR Code com seu WhatsApp")
    print("3. O bot começará a monitorar automaticamente")
    print("4. Pressione Ctrl+C para parar o bot")
    print()
    
    input("Pressione Enter para iniciar o bot...")
    
    try:
        bot.iniciar_bot()
    except KeyboardInterrupt:
        print("\nBot interrompido pelo usuário")

if __name__ == "__main__":
    main()