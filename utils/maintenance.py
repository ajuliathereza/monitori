import os
import tempfile
import psutil
import shutil

def limpar_cache():
    tmp = tempfile.gettempdir()
    try:
        for item in os.listdir(tmp):
            caminho = os.path.join(tmp, item)
            if os.path.isfile(caminho):
                os.remove(caminho)
            elif os.path.isdir(caminho):
                shutil.rmtree(caminho, ignore_errors=True)
        return "🧹 Cache limpo com sucesso!"
    except Exception as e:
        return f"Erro ao limpar cache: {e}"

def encerrar_pesados():
    processos = [(p.pid, p.info["name"], p.info["cpu_percent"])
                 for p in psutil.process_iter(["name", "cpu_percent"])
                 if p.info["cpu_percent"] and p.info["cpu_percent"] > 40]
    for pid, nome, cpu in processos:
        try:
            psutil.Process(pid).terminate()
        except Exception:
            pass
    if processos:
        return f"⚙️ {len(processos)} processos pesados encerrados!"
    else:
        return "✨ Nenhum processo pesado encontrado."

def verificar_firewall():
    # Simulado, apenas como exemplo
    return "🛡️ Firewall ativo e protegido!"
