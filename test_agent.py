import pytest
from agent import process_ticket

# Suite de 20 cas de tests métiers automatisés
TEST_SUITE = [
    # 16 cas nominaux (SUCCESS)
    ("J'ai oublié mon mot de passe", "SUCCESS", "GESTION_ACCES", "HAUTE"),
    ("Mon compte est bloqué suite à 3 essais", "SUCCESS", "GESTION_ACCES", "HAUTE"),
    ("Réinitialisation de mon mot de passe svp", "SUCCESS", "GESTION_ACCES", "HAUTE"),
    ("Problème de connexion au réseau local", "SUCCESS", "RESEAU", "MOYENNE"),
    ("Le wifi ne marche pas dans la salle B", "SUCCESS", "RESEAU", "MOYENNE"),
    ("Impossible de me connecter au réseau VPN", "SUCCESS", "RESEAU", "MOYENNE"),
    ("Panne totale de mon ordinateur", "SUCCESS", "MATERIEL", "CRITIQUE"),
    ("Ecran noir au démarrage de ma machine urgent", "SUCCESS", "MATERIEL", "CRITIQUE"),
    ("Mon PC a chauffé puis s'est éteint en panne", "SUCCESS", "MATERIEL", "CRITIQUE"),
    ("Comment demander une deuxième souris ?", "SUCCESS", "SUPPORT_GENERAL", "BASSE"),
    ("Demande d'information sur la charte IT", "SUCCESS", "SUPPORT_GENERAL", "BASSE"),
    ("Besoin d'aide pour configurer ma signature email", "SUCCESS", "SUPPORT_GENERAL", "BASSE"),
    ("Où se trouve le guide utilisateur d'imprimante", "SUCCESS", "SUPPORT_GENERAL", "BASSE"),
    ("Demande de mise à jour du navigateur", "SUCCESS", "SUPPORT_GENERAL", "BASSE"),
    ("Besoin d'un câble HDMI supplémentaire", "SUCCESS", "SUPPORT_GENERAL", "BASSE"),
    ("Question sur l'horaire du support informatique", "SUCCESS", "SUPPORT_GENERAL", "BASSE"),
    
    # 4 cas d'échecs / erreurs gérées (FAILURE)
    ("vide", "FAILURE", "UNKNOWN", "NONE"),
    ("", "FAILURE", "UNKNOWN", "NONE"),
    ("erreur_systeme crash base de donnees", "FAILURE", "LOGICIEL", "HAUTE"),
    ("erreur_systeme deconnexion serveur principal", "FAILURE", "LOGICIEL", "HAUTE")
]

@pytest.mark.parametrize("user_request, expected_status, expected_cat, expected_prio", TEST_SUITE)
def test_helpdesk_agent(user_request, expected_status, expected_cat, expected_prio):
    result = process_ticket(user_request)
    assert result["status"] == expected_status
    assert result["category"] == expected_cat
    assert result["priority"] == expected_prio