### **Introducción**
  Nsupdate es utilizado para enviar solicitudes dinámicas de DNS hacia un servidor DNS como se define en el RFC 2136. Permite añadir o eliminar registros de una zona son tener que editar manualmente los archivos de zona. Una sola solicitud de actualización puede contener varias solicitudes y añadir o eliminar más de un registro.

### **Requisitos**
   - BIND 
   - dnspython=2.4.2

### **Setup**
   - configurar los datos del Servidor DNS.
   ```shell
    DNS_IP_ADDRESS=
    KEY_NAME=
    KEY_SECRET=
    NAME_ZONE=
   ```
### **Uso**
```shell
source .virtualenv_python3
pip install -r requirements.txts
python3 app.py
```