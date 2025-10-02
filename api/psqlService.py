from psqlConfig import create_pool
from psqlModel import Etudiant, Presence, EtudPres

# ------- service Etudiant -------

async def service_get_all_etudiants():
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT * FROM etudiant;")
    await pool.close()
    return [Etudiant(**item) for item in result]

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