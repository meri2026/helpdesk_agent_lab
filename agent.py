import uuid
import time
import json
import os
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

LOG_FILE = "executions_log.json"

# ==========================================
# 🔔 MODULE D'ALERTES (GMAIL & SLACK)
# ==========================================

def send_email_alert(correlation_id, category, duration_ms, reason):
    """
    Envoie un email via le serveur SMTP de Gmail.
    Note : Nécessite un 'Mot de passe d'application' Google généré dans votre compte Gmail.
    """
    sender = "meriem.bahroud@gmail.com"
    receiver = "meriem.bahroud@gmail.com"
    app_password = "gkavkisixiaopuao"

    # Si les identifiants ne sont pas configurés, on simule l'envoi pour éviter le crash
    if sender == "votre_email@gmail.com":
        print(f"📧 [SIMULATION EMAIL] Alerte envoyée pour {correlation_id} (Raison: {reason})")
        return

    body = f"""🚨 ALERTE HELPDESK IT AGENT 🚨

Ticket ID   : {correlation_id}
Catégorie   : {category}
Latence     : {duration_ms} ms
Détection   : {reason}
Horodatage  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Merci de vérifier le tableau de bord de supervision.
"""

    msg = MIMEText(body)
    msg['Subject'] = f"🚨 ALERTE IT Helpdesk [{correlation_id}]"
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, app_password)
            server.sendmail(sender, receiver, msg.as_string())
        print(f"📧 Notification Email envoyée avec succès pour {correlation_id} !")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'envoi de l'email : {e}")


def check_and_trigger_alerts(log_entry):
    """
    Vérifie les métriques d'une exécution et déclenche les alertes si nécessaire.
    """
    status = log_entry["status"]
    duration_ms = log_entry["duration_ms"]
    correlation_id = log_entry["correlation_id"]
    category = log_entry["category"]
    error_msg = log_entry["error"]

    # 1. Alerte Échec (FAILURE)
    if status == "FAILURE":
        reason = f"Échec de traitement : {error_msg}"
        send_email_alert(correlation_id, category, duration_ms, reason)

    # 2. Alerte Latence SLA (> 1500 ms)
    elif duration_ms > 1500:
        reason = f"Dépassement du SLA de latence ({duration_ms} ms > 1500 ms)"
        send_email_alert(correlation_id, category, duration_ms, reason)


# ==========================================
# 🤖 LOGIQUE MÉTIER DE L'AGENT IT
# ==========================================

def generate_correlation_id():
    return f"TICKET-{uuid.uuid4().hex[:6].upper()}"

def process_ticket(user_request):
    correlation_id = generate_correlation_id()
    start_time = time.time()
    
    # Simulation du temps de traitement et des tokens
    time.sleep(random.uniform(0.1, 0.4))
    tokens_used = random.randint(350, 2200)
    
    req_clean = user_request.strip().lower()
    
    if not req_clean or req_clean == "vide":
        status = "FAILURE"
        category = "UNKNOWN"
        priority = "NONE"
        error_msg = "Ticket vide ou invalide"
        resolved_by = "FAILED"
    elif "erreur_systeme" in req_clean:
        status = "FAILURE"
        category = "LOGICIEL"
        priority = "HAUTE"
        error_msg = "Timeout sur la base de données de ticketing"
        resolved_by = "HUMAN_ESCALATION"
    elif "mot de passe" in req_clean or "compte" in req_clean:
        status = "SUCCESS"
        category = "GESTION_ACCES"
        priority = "HAUTE"
        error_msg = None
        resolved_by = "AGENT_AUTO"
    elif "connexion" in req_clean or "wifi" in req_clean or "réseau" in req_clean:
        status = "SUCCESS"
        category = "RESEAU"
        priority = "MOYENNE"
        error_msg = None
        resolved_by = "AGENT_AUTO"
    elif "panne" in req_clean or "urgent" in req_clean or "ecran noir" in req_clean:
        status = "SUCCESS"
        category = "MATERIEL"
        priority = "CRITIQUE"
        error_msg = None
        resolved_by = "HUMAN_ESCALATION"
    else:
        status = "SUCCESS"
        category = "SUPPORT_GENERAL"
        priority = "BASSE"
        error_msg = None
        resolved_by = "AGENT_AUTO"
        
    duration_ms = round((time.time() - start_time) * 1000, 2)
    
    # Structure de Log
    log_entry = {
        "correlation_id": correlation_id,
        "timestamp": datetime.now().isoformat(),
        "agent_version": "1.1.0",
        "environment": "production",
        "status": status,
        "category": category,
        "priority": priority,
        "resolved_by": resolved_by,
        "duration_ms": duration_ms,
        "tokens_used": tokens_used,
        "cost_usd": round(tokens_used * 0.000002, 6),
        "error": error_msg
    }
    
    # Enregistrement dans le fichier JSON
    save_log(log_entry)
    
    # Évaluation et déclenchement des alertes
    check_and_trigger_alerts(log_entry)
    
    return log_entry

def save_log(entry):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

if __name__ == "__main__":
    # Test manuel du script avec 3 requêtes (dont une erreur)
    print("🚀 Test de l'agent et du système d'alerte...\n")
    process_ticket("Mon mot de passe ne fonctionne plus")
    process_ticket("erreur_systeme crash serveur")
    process_ticket("Panne urgente sur ecran noir")
    print("\n✅ Execution terminée.")