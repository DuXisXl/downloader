from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import downloader

driver = webdriver.Chrome()

driver.get("https://web.whatsapp.com")

input("Escaneie o código QR e pressione Enter quando estiver pronto...")

ultimas_mensagens = []

noti = driver.find_elements(By.CLASS_NAME, '_2H6nH')

while True:    
    # Verifica se há notificações não lidas
    notificacoes = driver.find_elements(By.CLASS_NAME, '_2H6nH')

    if len(notificacoes) > 0:
        nome = ""
        ok = False
        notificacoes[0].click()
        time.sleep(2)
        mensagens = driver.find_elements(By.XPATH, '//*[@id="main"]//div[contains(@class, "message-in")]//span[contains(@class, "selectable-text")]')
        ultima_mensagem = ""
        ultima_mensagem = mensagens[-1].text
        penultima_mensagem_enviada = mensagens[-2].text
        if "reels" in ultima_mensagem:
            nome = downloader.download_reel(ultima_mensagem)
            ok = True
        if "reel" in ultima_mensagem:
            nome = downloader.download_reel(ultima_mensagem)
            ok = True
        if "youtube" in ultima_mensagem:
            campo_mensagem = driver.find_element(By.CLASS_NAME, '_3Uu1_')
            campo_mensagem.send_keys("Envie 1 para baixar o Video ou 2 para baixar o audio.")
            campo_mensagem.send_keys(Keys.RETURN)
            time.sleep(3)
            driver.refresh()
        if "1" in ultima_mensagem:
            nome = downloader.download_video(penultima_mensagem_enviada)
            ok = True
        if "2" in ultima_mensagem:
            nome = downloader.download_audio(penultima_mensagem_enviada)
            ok = True
        if "youtube" in penultima_mensagem_enviada:
            if ultima_mensagem != "1" and ultima_mensagem != "2":
                campo_mensagem = driver.find_element(By.CLASS_NAME, '_3Uu1_')
                campo_mensagem.send_keys("Não foi possivel reconhecer seu comando, mande o link novamente e refaça o procedimento.")
                campo_mensagem.send_keys(Keys.RETURN)
                time.sleep(2)
                driver.refresh()
        if ok == True:
            anexo_icon = driver.find_element(By.XPATH, '//div[@title="Anexar"]')
            anexo_icon.click()
            time.sleep(1)
            campo_arquivo = driver.find_element(By.XPATH, '//input[@type="file"]')
            diretorio_atual = os.getcwd()
            nome_video = nome
            print(os.path.join(diretorio_atual, nome_video))
            caminho_do_video = os.path.join(diretorio_atual, nome_video)
            campo_arquivo.send_keys(caminho_do_video)
            time.sleep(5)
            botao_enviar = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span')
            botao_enviar.click()
            print("Última mensagem enviada:", ultima_mensagem)
            time.sleep(60)
    else:
        print("Nenhuma mensagem nova.")

    time.sleep(20)

driver.quit()
