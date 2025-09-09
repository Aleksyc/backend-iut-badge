from psqlConfig import create_pool
from psqlModel import Etudiant, Presence

async def service_get_all_etudiants():
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT * FROM etudiant;")
    await pool.close()
    return [Etudiant(**item) for item in result]

async def service_get_all_presences():
    pool = await create_pool()
    async with pool.acquire() as connection:
        result = await connection.fetch("SELECT * FROM presence;")
    await pool.close()
    return [Presence(**item) for item in result]

async def service_insert_etudiant(etudiant: Etudiant):
    pool = await create_pool()
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO etudiant (nom_etu, prenom_etu, anne_etu, td_etu, tp_etu, id_carte_etu) VALUES ($1, $2, $3, $4, $5, $6);",
            etudiant.nom_etu,
            etudiant.prenom_etu,
            etudiant.anne_etu,
            etudiant.td_etu,
            etudiant.tp_etu,
            etudiant.id_carte_etu,
        )
    await pool.close()
    return etudiant

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