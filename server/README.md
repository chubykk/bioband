# BioBand

## Instalation

1. Tener `git`, `gh`, `pip` y `venv` instalados:

```bash
sudo apt install python3-pip python3-venv git gh -y
```

2. Autorizar la computadora con `gh` en el navegador:

```bash
gh auth login
```

3. Crear un entorno virtual

```bash
python3 -mp venv .bioband
```

4. Activar entorno virtual

```bash
source .bioband/bin/activate
```

5. Instalar requisitos

```bash
python3 -m pip install -r requirements.txt
```

6. Cuando se termine, desactivar entorno virtual

```bash
deactivate
```
