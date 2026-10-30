"""
WhatsApp Web Bot - Versão Final Otimizada
Autor: ChatBot Assistant
Data: 19/09/2025

Bot que responde automaticamente 'aguarde que em breve irei atender'
no WhatsApp Web usando Chrome.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import unquote
import time

class WhatsAppBotFinal:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.mensagem = "Aguarda que daqui a pouco responderei !"
        self.nomes_bloqueados = {"1TDSOS-2025", "ADS FIAP ON"}
        
    def iniciar_chrome(self):
        """Inicia o Chrome de forma otimizada"""
        try:
            print("🚀 Iniciando Chrome...")
            
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 20)
            
            print("✅ Chrome iniciado!")
            return True
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def entrar_whatsapp(self):
        """Entra no WhatsApp Web"""
        try:
            print("📱 Abrindo WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            time.sleep(8)
            
            # Verifica se precisa fazer login
            try:
                qr = self.driver.find_element(By.XPATH, "//canvas")
                print("📸 QR Code detectado! Escaneie com seu celular.")
                
                # Aguarda login (QR desaparecer)
                while True:
                    try:
                        self.driver.find_element(By.XPATH, "//canvas")
                        time.sleep(2)
                    except:
                        print("✅ Login realizado!")
                        break
            except:
                print("✅ Já logado!")
            
            time.sleep(5)
            print("✅ WhatsApp Web carregado!")
            return True
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def buscar_conversas(self):
        """Busca conversas não lidas"""
        try:
            # Seletor simples para conversas
            conversas = self.driver.find_elements(By.XPATH, "//div[@role='listitem']")
            return conversas[:5]  # Primeiras 5 conversas
        except:
            return []

    def normalizar_nome(self, texto):
        """Remove quebras e espaços extras para comparar nomes."""
        if not texto:
            return ""
        return " ".join(texto.replace("\n", " ").split())

    def conversa_bloqueada(self, nome):
        """Verifica se o nome informado está na lista de bloqueados."""
        normalizado = self.normalizar_nome(nome).lower()
        for bloqueado in self.nomes_bloqueados:
            if bloqueado.lower() in normalizado and normalizado:
                return True
        return False
    
    def obter_nome_chat(self):
        """Retorna o nome/título da conversa atualmente aberta."""
        if not self.wait:
            return "Conversa desconhecida"

        seletores = [
            "//header//span[@data-testid='conversation-header-title']",
            "//header//span[contains(@data-testid,'conversation-info-header')]",
            "//header//h1",
            "//header//span[contains(@class,'selectable-text')]"
        ]

        for xpath in seletores:
            try:
                elemento = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                texto = elemento.text.strip()
                if texto:
                    return texto
            except TimeoutException:
                continue
            except Exception:
                continue

        return "Conversa desconhecida"

    def identificar_tipo_conversa_atual(self):
        """Classifica a conversa aberta como contato, grupo ou indefinida."""
        identificadores = []

        try:
            hash_value = self.driver.execute_script("return window.location.hash || '';")
            if hash_value:
                identificadores.append(unquote(hash_value))
        except Exception:
            pass

        try:
            current_url = unquote(self.driver.current_url)
            if current_url:
                identificadores.append(current_url)
        except Exception:
            pass

        for identificador in identificadores:
            if "@g.us" in identificador or "@broadcast" in identificador:
                return "grupo"
            if "@c.us" in identificador or "@s.whatsapp.net" in identificador:
                return "contato"

        try:
            header = self.wait.until(EC.presence_of_element_located((By.XPATH, "//header")))
            header_texto = (header.get_attribute("innerText") or "").lower()
            if any(palavra in header_texto for palavra in ["participantes", "grupo", "administrador"]):
                return "grupo"
        except TimeoutException:
            pass
        except Exception:
            pass

        return "contato"

    def enviar_resposta(self, conversa):
        """Envia resposta automática apenas para conversas individuais."""
        try:
            nome_lista = self.normalizar_nome(conversa.get_attribute("aria-label") or "")
            if self.conversa_bloqueada(nome_lista):
                print(f"🚫 Ignorado na lista: '{nome_lista}' (bloqueado manualmente).")
                return {"processado": True, "acao": "ignorado", "tipo": "bloqueado", "nome": nome_lista}

            conversa.click()
            time.sleep(2)

            nome_chat = self.normalizar_nome(self.obter_nome_chat())

            if self.conversa_bloqueada(nome_chat):
                print(f"🚫 Ignorado no chat: '{nome_chat}' (bloqueado manualmente).")
                return {"processado": True, "acao": "ignorado", "tipo": "bloqueado", "nome": nome_chat}

            caixa = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")))

            caixa.click()
            caixa.clear()
            caixa.send_keys(self.mensagem)
            caixa.send_keys(Keys.ENTER)

            destinatario = nome_chat or nome_lista or "Contato desconhecido"
            print(f"✅ Mensagem enviada para '{destinatario}'!")
            return {"processado": True, "acao": "enviado", "tipo": "contato", "nome": destinatario}

        except TimeoutException as e:
            print(f"❌ Tempo excedido ao localizar elementos: {e}")
            return {"processado": False, "acao": "erro", "detalhe": str(e)}
        except Exception as e:
            print(f"❌ Erro ao enviar: {e}")
            return {"processado": False, "acao": "erro", "detalhe": str(e)}
    
    def monitorar(self):
        """Monitora mensagens em loop simples"""
        print("🤖 Monitorando mensagens...")
        print("🛑 Pressione Ctrl+C para parar")
        
        processadas = set()
        
        while True:
            try:
                conversas = self.buscar_conversas()
                print(f"📨 Verificando {len(conversas)} conversas...")
                
                for i, conversa in enumerate(conversas):
                    conv_id = f"conv_{i}"
                    
                    if conv_id not in processadas:
                        print(f"💬 Processando conversa {i+1}...")
                        
                        resultado = self.enviar_resposta(conversa)
                        if isinstance(resultado, dict) and resultado.get("processado"):
                            processadas.add(conv_id)

                        time.sleep(2)
                
                print("⏳ Aguardando 15 segundos...")
                time.sleep(15)
                
            except KeyboardInterrupt:
                print("\\n🛑 Parando bot...")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
                time.sleep(10)
    
    def executar(self):
        """Executa o bot completo"""
        try:
            print("🤖 WHATSAPP BOT - RESPOSTA AUTOMÁTICA")
            print("=" * 45)
            print("📋 O que o bot faz:")
            print("1. Abre o Chrome automaticamente")
            print("2. Acessa WhatsApp Web")
            print("3. Responde automaticamente com:")
            print(f"   '{self.mensagem}'")
            print("4. Monitora continuamente")
            print("=" * 45)
            
            input("▶️ Pressione Enter para iniciar...")
            
            if not self.iniciar_chrome():
                return
                
            if not self.entrar_whatsapp():
                return
                
            self.monitorar()
            
        except Exception as e:
            print(f"❌ Erro geral: {e}")
        finally:
            if self.driver:
                print("🔒 Fechando...")
                self.driver.quit()
                print("✅ Finalizado!")

def main():
    bot = WhatsAppBotFinal()
    bot.executar()

if __name__ == "__main__":
    main()