from dataclasses import dataclass
import datetime
import glob
from jinja2 import Template
import os.path
import logging
from PrimeBot.IntegracaoSendGrid import IntegracaoSendGrid

@dataclass
class EmailAlert:
    """
        Envio de email para alertar falhas no funcionamento de um processo.

        Atributos: 
            api_key (str): Chave válida da API Sendgrid.
            remetente (str): Endereço de email cadastrado no SendGrid para envio das mensagens.
            destinatario (str): Endereço de email que receberá a mensagem.
            nome_projeto (str): Nome do projeto.
            pasta_screenshots (str): Caminho da pasta no projeto onde ficam os screenshots.
    """

    api_key: str = ''
    remetente: str = ''  
    destinatario: str = '' 
    nome_projeto: str = ''
    pasta_screenshots: str = None  

    def __post_init__(self) -> None:
        """
            Método pós-inicialização que realiza a conexão com a API do sendgrid.
        """
        self.sg = IntegracaoSendGrid(self.api_key, self.remetente)

    def converter_texto_para_html(self, mensagem: str = '') -> str:
        """
            Cria uma mensagem em HTML.

            Atributos:
                mensagem (str): Mensagem para ser formatada em HTML.
            
            Retorna:
                str: Mensagem formatada em HTML.
        """
        list_dict = []
        html = f'''{mensagem}'''
        template = Template(html)
        body_email = template.render(list=list_dict)
        return body_email
    
    def encontrar_ultimo_arquivo_pasta(self, path_pasta) -> str:
        """
            Busca o arquivo inserido mais recente na pasta.

            Atributos:
                path_pasta (str): Caminho da pasta.
            
            Retorna: 
                str: Caminho do arquivo mais recente.
        """
        files = glob.glob(path_pasta + '\*')
        item_recente = max(files, key=os.path.getctime)
        return item_recente
    
    def enviar_alerta_de_erro(self, task: str, keyword:str ,mensagem_erro: str) -> None:
        """
            Dispara um email de alerta de erro, caso um processo seja interrompido antes da conclusão do processo.

            Atributos:
                task (str): Nome da task que falhou.
                keyword (str): Nome da keyword processada no momento da falha.
                mensagem_erro (str): Mensagem retornada pelo processo detalhando o erro.
        """
        data = datetime.datetime.now().strftime('%d/%m/%Y')
        hora = datetime.datetime.now().strftime('%H:%M:%S')
        mensagem = f'<p>Olá, tudo bem?</p><p>Houve um erro durante a execução do processo: <b><font color="#FF0000">{self.nome_projeto}</font></b>, que ocasionou a interrupção do mesmo antes de concluir o processo, segue informações:</p><p><b>Data:</b> {data};</p><p><b>Hora:</b> {hora};</p><p><b>Task:</b> {task};</p><p><b>Keyword:</b> {keyword};</p><p><b>Detalhe retornado do erro:</b> {mensagem_erro}.</p>'
        html = self.converter_texto_para_html(mensagem)
        to= self.destinatario
        email = self.sg.create_message(to, f'Azul RPA Falha no projeto: {self.nome_projeto}', html)
        
        # Verifica se existe screenshot
        try:
            archives = os.listdir(self.pasta_screenshots)
            if len(archives) > 0:
                screenshot = self.encontrar_ultimo_arquivo_pasta(self.pasta_screenshots)
                email = self.sg.add_attachment(email, screenshot, 'image/png', 'attachment', 'anexo')
        except Exception as error:
            logging.error(f'Erro ao acessar os arquivos da pasta de screenshots, detalhe: {error}!')
        
        result = self.sg.send_email(email)
        logging.info(result, also_console=True)