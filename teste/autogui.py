import pyautogui
import time

# Define um intervalo entre cada ação
intervalo = 0.5
começa = 5.30
# Função para digitar texto e esperar
def digitar_com_espera(texto, intervalo):
    pyautogui.write(texto)
    time.sleep(intervalo)

# Sequência de comandos
def executar_sequencia():

    # 1. Ctrl + Tab
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(intervalo)

    # 2. Shift + F10
    pyautogui.hotkey('shift', 'f10')
    time.sleep(começa)

    largura_tela, altura_tela = pyautogui.size()
    pyautogui.moveTo(largura_tela // 2, altura_tela // 4 * 3)  # Mover para 1/4 da altura
    time.sleep(intervalo)  # Esperar um pouco antes de clicar
    pyautogui.click()  # Clique com o botão esquerdo
    time.sleep(intervalo)

    # 3. 'pt'
    # 4. 'pt' e pressionar Enter
    digitar_com_espera('pt', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

    # 5. 1 e pressionar Enter
    digitar_com_espera('1', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

    # 6. 1 e pressionar Enter
    digitar_com_espera('1', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

    # 7. 2 e pressionar Enter
    digitar_com_espera('2', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

    # 8. 'miguel' e pressionar Enter
    digitar_com_espera('miguel', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

    # 9. Shift (pressiona e solta Shift)
    pyautogui.press('shift')
    time.sleep(intervalo)

    # 10. 'drones de campo' e pressionar Enter
    digitar_com_espera('drones de campo', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

    digitar_com_espera('shift', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

    # 11. '6000' e pressionar Enter
    digitar_com_espera('6000', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

    # 12. 'nacional' e pressionar Enter
    digitar_com_espera('nacional', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

    # 13. '12' e pressionar Enter
    digitar_com_espera('12', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

    # 14. '9000' e pressionar Enter
    digitar_com_espera('9000', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

    # 15. 'no' e pressionar Enter
    digitar_com_espera('no', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

    # 16. 'empresas de agropecuaria' e pressionar Enter
    digitar_com_espera('empresas de agropecuaria', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

    # 17. 'sim' e pressionar Enter
    digitar_com_espera('sim', intervalo)
    pyautogui.press('enter')
    time.sleep(intervalo)

# Executa a sequência
executar_sequencia()
