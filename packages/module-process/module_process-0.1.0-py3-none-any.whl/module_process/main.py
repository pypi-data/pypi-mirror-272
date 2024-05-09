from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

class AzureBlobManager:
    stages = {0: 'raw', 1: 'improvement', 2: 'ocr', 3: 'llm', 4: 'validation'}

    def __init__(self, stage_num, account_url="https://smartocrdata.blob.core.windows.net", 
                 sas_token="fK5yfnGPaRCbtwNA6NIMHp8BrDS4sYEKt8USz7ldR4aBZ2v1Aq+8ybNXtLQd7/LjFoz5/ts9Uwm8+AStlWrekw==", 
                 container_name='cliente-0-data'):
        self.account_url = account_url
        self.sas_token = sas_token
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient(account_url=self.account_url, credential=self.sas_token)
        self.container_client = self.blob_service_client.get_container_client(container_name)
        self.stage_num = stage_num

    def ensure_container(self):
        """Garante que o container exista no Azure Blob Storage."""
        try:
            self.container_client.create_container()
            print(f"Container '{self.container_name}' criado.")
        except Exception as e:
            print(f"Container '{self.container_name}' já existe ou erro: {e}")

    def delete_documents(self, blob_urls):
        """Deleta documentos com base em uma lista de URLs completos."""
        for url in blob_urls:
            try:
                # Verifica se o URL já contém um token; se não, adiciona o SAS Token
                if '?' not in url:
                    url = f"{url}?{self.sas_token}"
                    
                # Criação do BlobClient com o URL completo, incluindo o SAS Token
                blob_client = BlobClient.from_blob_url(url)
                blob_client.delete_blob()
                print(f"Documento deletado com sucesso: {url}")
            except Exception as e:
                print(f"Erro ao deletar o documento {url}: {e}")
    
    def create_client_directories(self, protocol_num):
        """ Cria subdiretórios para cada etapa de processamento dentro do container """
        stages = ['raw', 'improvement', 'ocr', 'llm', 'validation']
        for stage in stages:
            # Criando um blob dummy para estabelecer a estrutura de diretório
            blob_name = f"{protocol_num}/{stage}/dummy.txt"
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.upload_blob("Initialization", overwrite=True)
            print(f"Subdiretório {blob_name} criado.")

    def save_document(self, protocol_num, file_binary_data):
        stage = self.stages.get(self.stage_num)
        if not stage:
            raise ValueError("Invalid stage number provided")

        next_file_name = self.get_next_file_name(protocol_num)
        blob_client = self.container_client.get_blob_client(next_file_name)

        blob_client.upload_blob(file_binary_data, overwrite=True)
        print(f"Documento salvo como {next_file_name}")
        return blob_client.url
    
    def get_next_file_name(self, protocol_num):
        stage = self.stages.get(self.stage_num)
        prefix = f"{protocol_num}/{stage}/"
        blob_list = self.container_client.list_blobs(name_starts_with=prefix)
        max_index = 0
        for blob in blob_list:
            parts = blob.name.rsplit('_', 1)
            if len(parts) > 1 and parts[1].isdigit():
                index = int(parts[1])
                if index > max_index:
                    max_index = index
        next_index = max_index + 1
        return f"{prefix}{stage}_{next_index}"

    def download_document(self, blob_url):
        """Baixa um documento diretamente usando o URL completo do blob."""
        try:
            # Criando um BlobClient diretamente a partir do URL do blob
            blob_client = BlobClient.from_blob_url(blob_url)
            downloader = blob_client.download_blob()
            data = downloader.readall()
            return data
        except Exception as e:
            print(f"Erro ao baixar o documento: {e}")

# # Example usage
# if __name__ == "__main__":
    
#     manager = AzureBlobManager()
#     protocol_num = "protocol123"

#     # Example to create directories for a new client
#     manager.create_client_directories(protocol_num)

#     # Example to save a document
#     # base64_data = base64.b64encode(b"Your document data here").decode('utf-8')
#     base64_data = ""
#     link = manager.save_document(protocol_num, base64_data, 1)  # 1 for 'raw'

#     print("Document saved at:", link)

#     # Example to download a document
#     downloaded_data = manager.download_document(link)
#     print("Downloaded Base64 Data:", downloaded_data)

#     manager.delete_documents([link])


