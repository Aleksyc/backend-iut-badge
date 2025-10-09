from psqlConfig import create_pool
from psqlModel import Etudiant, Presence, EtudPres
import datetime

# ------- service Etudiant -------

async def service_get_all_etudiants():
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT * FROM etudiant;")
    await pool.close()
    return [Etudiant(**item) for item in result]

async def service_search_etudiants(params: dict):
    pool = await create_pool()
    async with pool.acquire() as connection:
        if params and params["datetime_pres_start"] != "" and params["datetime_pres_end"] != "":
            date_start = datetime.datetime.strptime(params["datetime_pres_start"], "%Y-%m-%d").date()
            date_end = datetime.datetime.strptime(params["datetime_pres_end"], "%Y-%m-%d").date()
            query = f"SELECT e.id_etu,e.nom_etu,e.prenom_etu,e.anne_etu,e.td_etu,e.tp_etu, p.datetime_pres, CASE WHEN p.id_carte_etu IS NOT NULL THEN 'Présent' ELSE 'Absent' END AS statut_presence FROM etudiant e CROSS JOIN (SELECT jour FROM generate_series('{date_start}'::date, '{date_end}'::date, interval '1 day') AS g(jour) WHERE EXTRACT(ISODOW FROM jour) NOT IN (6, 7)) AS d LEFT JOIN presence p ON e.id_carte_etu = p.id_carte_etu AND p.datetime_pres::date = d.jour"
            values = []
            i = 1
            for key, value in params.items():
                if key != "datetime_pres_start" and key != "datetime_pres_end":
                    if i == 1 : query += f" WHERE {key} = ${i}"
                    else: query += f" AND {key} = ${i}"
                    values.append(value)
                    i += 1
            query += "ORDER BY d.jour;"
        result = await connection.fetch(query, *values)
    await pool.close()
    return [EtudPres(**item) for item in result]

async def service_get_count_etudiants():
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT COUNT(*) FROM etudiant;")
    await pool.close()
    return result[0]["count"]

async def service_get_count_etudiants_actifs():
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT COUNT(DISTINCT id_carte_etu) AS nb_etudiants_actifs FROM presence WHERE datetime_pres::date = CURRENT_DATE;")
    await pool.close()
    return result[0]["nb_etudiants_actifs"]

async def service_get_etudiants_presences():
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT id_etu, nom_etu, prenom_etu, anne_etu, td_etu, tp_etu, datetime_pres FROM etudiant INNER JOIN presence ON etudiant.id_carte_etu = presence.id_carte_etu;")
    await pool.close()
    return [EtudPres(**item) for item in result]

async def service_delete_etudiant(id_etu: int):
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.execute("DELETE FROM etudiant WHERE id_etu = $1;", id_etu)
    await pool.close()
    return {"message": f"Étudiant avec l'id {id_etu} supprimé."}

# ------- service Presence -------

async def service_get_count_day():
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT COUNT(*) AS nb_badges FROM presence WHERE datetime_pres::date = CURRENT_DATE;")
    await pool.close()
    return result[0]["nb_badges"]

async def service_get_count_week():
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT COUNT(*) AS nb_badges FROM presence WHERE datetime_pres >= date_trunc('week', CURRENT_DATE) AND datetime_pres < date_trunc('week', CURRENT_DATE) + interval '1 week';")
    await pool.close()
    return result[0]["nb_badges"]

async def service_get_all_presences():
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT * FROM presence;")
    await pool.close()
    return [Presence(**item) for item in result]

async def service_insert_presence(presence: Presence):
    pool = await create_pool()
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO presence (id_carte_etu, datetime_pres, type_pres) VALUES ($1, $2, $3);",
            presence.id_carte_etu,
            presence.datetime_pres,
            presence.type_pres,
        )
    await pool.close()
    return presence