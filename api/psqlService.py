from psqlConfig import create_pool
from psqlModel import Etudiant, EtudiantCreate, Presence, EtudPres
import datetime

# =================== Service Etudiant ===================

async def service_get_all_etudiants():
    """
    Récupère tous les étudiants de la base de données.
    return: Liste d'objets Etudiant.
    """
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT * FROM etudiant;")
    await pool.close()
    return [Etudiant(**item) for item in result]

async def service_get_etudiants_presences():
    """
    Récupère les présences associées à chaque étudiant.
    return: Liste d'objets EtudPres (étudiant + présence).
    """
    pool = await create_pool()
    async with pool.acquire() as connection:
        query = "SELECT e.id_etu,e.nom_etu,e.prenom_etu,e.anne_etu,e.td_etu,e.tp_etu, CASE WHEN p.id_carte_etu IS NOT NULL THEN p.datetime_pres ELSE d.jour::timestamp END AS datetime_pres, CASE WHEN p.id_carte_etu IS NOT NULL THEN 'Présent' ELSE 'Absent' END AS statut_presence FROM etudiant e CROSS JOIN (SELECT jour FROM generate_series('2025-10-20'::date, to_char(CURRENT_DATE, 'YYYY-MM-DD')::date, interval '1 day') AS g(jour) WHERE EXTRACT(ISODOW FROM jour) NOT IN (6, 7)) AS d LEFT JOIN presence p ON e.id_carte_etu = p.id_carte_etu AND p.datetime_pres::date = d.jour ORDER BY d.jour DESC;"
        values = []
        result = await connection.fetch(query, *values)
    await pool.close()
    return [EtudPres(**item) for item in result]

async def service_insert_etudiant(etudiant: EtudiantCreate):
    """
    Insère un nouvel étudiant dans la base de données.
    param etudiant: Données de l'étudiant à insérer.
    return: L'objet Etudiant inséré.
    """
    pool = await create_pool()
    async with pool.acquire() as connection:
        row = await connection.fetchrow(
            "INSERT INTO etudiant (nom_etu, prenom_etu, anne_etu, td_etu, tp_etu, id_carte_etu) "
            "VALUES ($1, $2, $3, $4, $5, $6) RETURNING id_etu, nom_etu, prenom_etu, anne_etu, td_etu, tp_etu, id_carte_etu;",
            etudiant.nom_etu,
            etudiant.prenom_etu,
            etudiant.anne_etu,
            etudiant.td_etu,
            etudiant.tp_etu,
            etudiant.id_carte_etu,
        )
    await pool.close()
    return Etudiant(**row)

async def service_update_etudiant(id_etu: int, etudiant: EtudiantCreate):
    """
    Met à jour les informations d'un étudiant existant.
    param id_etu: ID de l'étudiant à modifier.
    param etudiant: Nouvelles données de l'étudiant.
    return: L'objet Etudiant mis à jour.
    """
    pool = await create_pool()
    async with pool.acquire() as connection:
        row = await connection.fetchrow(
            "UPDATE etudiant SET nom_etu = $1, prenom_etu = $2, anne_etu = $3, td_etu = $4, tp_etu = $5, id_carte_etu = $6 "
            "WHERE id_etu = $7 RETURNING id_etu, nom_etu, prenom_etu, anne_etu, td_etu, tp_etu, id_carte_etu;",
            etudiant.nom_etu,
            etudiant.prenom_etu,
            etudiant.anne_etu,
            etudiant.td_etu,
            etudiant.tp_etu,
            etudiant.id_carte_etu,
            id_etu,
        )
    await pool.close()
    return Etudiant(**row)

async def service_get_count_etudiants():
    """
    Retourne le nombre total d'étudiants dans la base.
    return: Entier du nombre d'étudiants.
    """
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT COUNT(*) FROM etudiant;")
    await pool.close()
    return result[0]["count"]

async def service_get_count_etudiants_actifs():
    """
    Retourne le nombre d'étudiants actifs aujourd'hui (ayant badgé).
    return: Entier du nombre d'étudiants actifs.
    """
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT COUNT(DISTINCT id_carte_etu) AS nb_etudiants_actifs FROM presence WHERE datetime_pres::date = CURRENT_DATE;")
    await pool.close()
    return result[0]["nb_etudiants_actifs"]

async def service_delete_etudiant(id_etu: int):
    """
    Supprime un étudiant selon son ID.
    param id_etu: ID de l'étudiant à supprimer.
    return: Message de confirmation.
    """
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.execute("DELETE FROM etudiant WHERE id_etu = $1;", id_etu)
    await pool.close()
    return {"message": f"Étudiant avec l'id {id_etu} supprimé."}

async def service_get_etudiant_by_id(id_etu: int):
    """
    Récupère un étudiant selon son ID.
    param id_etu: ID de l'étudiant à récupérer.
    return: Objet Etudiant correspondant.
    """
    pool = await create_pool()
    async with pool.acquire() as connection:
        row = await connection.fetchrow("SELECT * FROM etudiant WHERE id_etu = $1;", id_etu)
    await pool.close()
    return Etudiant(**row)

# =================== Service Presence ===================

async def service_get_count_day():
    """
    Retourne le nombre de badges (présences) du jour.
    return: Entier du nombre de badges aujourd'hui.
    """
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT COUNT(*) AS nb_badges FROM presence WHERE datetime_pres::date = CURRENT_DATE;")
    await pool.close()
    return result[0]["nb_badges"]

async def service_get_presence_by_id(id_etu: int):
    """
    Récupère une présence selon l'ID d'un étudiant.
    param id_etu: ID de l'étudiant à récupérer.
    return: Objet Presence correspondant.
    """
    pool = await create_pool()
    async with pool.acquire() as connection:
        query = "SELECT e.id_etu,e.nom_etu,e.prenom_etu,e.anne_etu,e.td_etu,e.tp_etu, CASE WHEN p.id_carte_etu IS NOT NULL THEN p.datetime_pres ELSE d.jour::timestamp END AS datetime_pres, CASE WHEN p.id_carte_etu IS NOT NULL THEN 'Présent' ELSE 'Absent' END AS statut_presence FROM etudiant e CROSS JOIN (SELECT jour FROM generate_series('2025-10-20'::date, to_char(CURRENT_DATE, 'YYYY-MM-DD')::date, interval '1 day') AS g(jour) WHERE EXTRACT(ISODOW FROM jour) NOT IN (6, 7)) AS d LEFT JOIN presence p ON e.id_carte_etu = p.id_carte_etu AND p.datetime_pres::date = d.jour WHERE e.id_etu = $1 ORDER BY d.jour DESC;"
        row = await connection.fetch(query, id_etu)
    await pool.close()
    return [EtudPres(**item) for item in row]

async def service_get_count_week():
    """
    Retourne le nombre de badges (présences) de la semaine courante.
    return: Entier du nombre de badges cette semaine.
    """
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT COUNT(*) AS nb_badges FROM presence WHERE datetime_pres >= date_trunc('week', CURRENT_DATE) AND datetime_pres < date_trunc('week', CURRENT_DATE) + interval '1 week';")
    await pool.close()
    return result[0]["nb_badges"]

async def service_get_all_presences():
    """
    Récupère toutes les présences enregistrées.
    return: Liste d'objets Presence.
    """
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT * FROM presence;")
    await pool.close()
    return [Presence(**item) for item in result]

async def service_insert_presence(presence: Presence):
    """
    Insère une nouvelle présence dans la base de données.
    param presence: Données de la présence à insérer.
    return: L'objet Presence inséré.
    """
    pool = await create_pool()
    async with pool.acquire() as connection:
        row = await connection.fetchrow(
            "INSERT INTO presence (id_carte_etu, datetime_pres) VALUES ($1, $2) RETURNING *;",
            presence.id_carte_etu,
            presence.datetime_pres,
        )
    await pool.close()
    return Presence(**row)