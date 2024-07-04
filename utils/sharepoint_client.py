from requests import request

class SharepointClient:
    '''
    Clase para interactuar con Sharepoint
    - Envío de archivos a sharepoint:
        - Se debe enviar el archivo a Sharepoint y obtener el ID del archivo
        - Con el ID del archivo se actualiza los metadatos
    '''

    def __init__(self):
        self.site_id = "site_id"
        self.library_name = "library_name"
        self.item_id = "item_id"

    
    def get_create_url(self, file_path, file_name, access_token):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/octet-stream",
        }
        create_url = f"https://graph.microsoft.com/v1.0/drives/{self.library_name}/items/root:/{file_name}:/content"

        response = request.put(create_url, headers = headers, data = file_path)
        if response.status_code in [200, 201]:
            file_data = response.json()
            file_id = file_data.get("id")
            return file_id
        else:
            print("Error al cargar el archivo en Sharepoint", response.status_code, response.text)
            return None
        
    def update_metadata_sharepoint(self, file_id, metadata, access_token):
        '''
        Actualiza los metadatos de un archivo en Sharepoint
        Los metadatos viene por parámetro en formato JSON desde el Endpoint
        Se pone este a manera de ejemplo
        '''
        metadata = {
            "fields":{
                "Soporte": "PAPEL",
            }
        }

        update_url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/drives/{self.library_name}/items/{file_id}/listItem/"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = request.patch(update_url, headers=headers, json=metadata)
        if response.status_code in [200, 201]:
            print("Metadatos actualizados correctamente")
            return True
        else:
            print("Error al actualizar los metadatos", response.status_code, response.text)
            return False
        

