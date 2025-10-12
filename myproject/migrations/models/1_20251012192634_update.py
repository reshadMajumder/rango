from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "student" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "first_name" VARCHAR(100) NOT NULL,
    "last_name" VARCHAR(100) NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "age" INT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "student";"""


MODELS_STATE = (
    "eJztlmtv2jAUhv9KlE+d1FVtRi/at5QylWnAVLKLWlWRSUywcOw0dtaiiv9eH+ceLisT26"
    "jEN/Ke99jnPPj2bIbcx1Qc2Tgm3sT8aDybDIVY/WhEDg0TRVGpgyDRiGorKj0jIWPkSaWO"
    "ERVYST4WXkwiSThTKksoBZF7ykhYUEoJIw8JdiUPsJzgWAXu7pVMmI+fsMg/o6k7Jpj6tV"
    "KJD3Nr3ZWzSGtdJj9pI8w2cj1Ok5CV5mgmJ5wVbsIkqAFmOEYSw/AyTqB8qC7rM+8orbS0"
    "pCVWcnw8RgmVlXZfycDjDPipaoRuMIBZ3lsnrfPWxYez1oWy6EoK5Xyetlf2niZqAn3HnO"
    "s4kih1aIwlt184FlDSArz2BMXL6VVSGghV4U2EObB1DHOhhFgunC1RDNGTSzELJCxw6/R0"
    "DbPv9k372r45UK530A1Xizld4/0sZKUxAFuChK2xAcTM/jYBnhwfvwKgcq0EqGN1gGpGid"
    "M9WIf4eTjoL4dYSWmA/MZUg3c+8eShQYmQ97uJdQ1F6BqKDoV4oFV4Bz37Z5Nr+8vgUlPg"
    "QgaxHkUPcKkYw5E5nlY2Pwgj5E0fUey7CxFu8VXexVBohU0FMRRoVtAx9JddIkOZ+PBfLb"
    "lf8tDaC0ZUTPsb5g3dMGMSC+nqrw3Ox3rW/pgscFL0BzRrSXuYBUwcIkI3AVkkbAfiX9/b"
    "/+DdEyxZiSvPxcz9+4NxR5bgVs7GyhsnxtCfi5Y8c65URJIQr3jq1DIb/Pws9Sj/saM0VQ"
    "/+gNFZttDXoHO6vc7QsXtfa0+gK9vpQMTS6qyhHpw11m0xiPGj61wb8GncDvqd5kup8Dm3"
    "JtSEEsldxh9d5Ff2ZK7mYP7vw2r+AjDOAD0="
)
