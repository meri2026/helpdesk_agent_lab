import uuid
import time
import json
import os
import random
from datetime import datetime

LOG_FILE = "executions_log.json"

def generate_correlation_id():
    return f"TICKET-{uuid.uuid4().hex[:6].upper()}"

def process_ticket(user_request):
    correlation_id = generate_correlation_id()
    start_time = time.time()
    
    # Simulation du temps de traitement et des tokens
    time.sleep(random.uniform(0.1, 0.4))
    tokens_used = random.randint(350, 2200)
    
    req_clean = user_request.strip().lower()
    
    # Logique métier Helpdesk IT (Ordre de priorité ajusté)
    if not req_clean or req_clean == "vide":
        status = "FAILURE"
        category = "UNKNOWN"
        priority = "NONE"
        error_msg = "Ticket vide ou invalide"
    elif "erreur_systeme" in req_clean:
        status = "FAILURE"
        category = "LOGICIEL"
        priority = "HAUTE"
        error_msg = "Timeout sur la base de données de ticketing"
    elif "mot de passe" in req_clean or "compte" in req_clean:
        status = "SUCCESS"
        category = "GESTION_ACCES"
        priority = "HAUTE"
        error_msg = None
    elif "connexion" in req_clean or "wifi" in req_clean or "réseau" in req_clean:
        status = "SUCCESS"
        category = "RESEAU"
        priority = "MOYENNE"
        error_msg = None
    elif "panne" in req_clean or "urgent" in req_clean or "ecran noir" in req_clean:
        status = "SUCCESS"
        category = "MATERIEL"
        priority = "CRITIQUE"
        error_msg = None
    else:
        status = "SUCCESS"
        category = "SUPPORT_GENERAL"
        priority = "BASSE"
        error_msg = None
        
    duration_ms = round((time.time() - start_time) * 1000, 2)
    
    # Structure de Log
    log_entry = {
        "correlation_id": correlation_id,
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "category": category,
        "priority": priority,
        "duration_ms": duration_ms,
        "tokens_used": tokens_used,
        "cost_usd": round(tokens_used * 0.000002, 6),
        "error": error_msg
    }
    
    save_log(log_entry)
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