import datetime

from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
)

db = SqliteDatabase(
    None,
    pragmas={
        "journal_mode": "wal",
        "foreign_keys": 1,
    },
)

ESPECIALIDADES = [
    "CLINICA MEDICA",
    "PEDIATRIA",
    "CARDIOLOGIA",
    "DERMATOLOGIA",
    "GINECOLOGIA",
    "TRAUMATOLOGIA",
    "NEUROLOGIA",
    "PSIQUIATRIA",
    "OFTALMOLOGIA",
    "OTORRINOLARINGOLOGIA",
    "UROLOGIA",
]

ESTADOS = ["RESERVADO", "ATENDIDO", "CANCELADO", "AUSENTE"]


class BaseModel(Model):
    class Meta:
        database = db


class ObraSocial(BaseModel):
    id = AutoField(primary_key=True)
    nombre = TextField(unique=True)
    creado_el = DateTimeField(default=datetime.datetime.now)
    actualizado_el = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "obras_sociales"


class Paciente(BaseModel):
    id = AutoField(primary_key=True)
    nombre = TextField()
    cuit = TextField(unique=True)
    fecha_nacimiento = DateField()
    obra_social = ForeignKeyField(ObraSocial, column_name="obra_social_id", backref="pacientes", null=True)
    creado_el = DateTimeField(default=datetime.datetime.now)
    actualizado_el = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "pacientes"


class Medico(BaseModel):
    id = AutoField(primary_key=True)
    nombre = TextField()
    especialidad = CharField(choices=ESPECIALIDADES)
    matricula = TextField(unique=True)
    activo = BooleanField(default=True)
    creado_el = DateTimeField(default=datetime.datetime.now)
    actualizado_el = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "medicos"


class Turno(BaseModel):
    id = AutoField(primary_key=True)
    paciente = ForeignKeyField(Paciente, column_name="paciente_id", backref="turnos")
    medico = ForeignKeyField(Medico, column_name="medico_id", backref="turnos")
    fecha = DateField()
    horario = TextField()
    estado = CharField(choices=ESTADOS, default="RESERVADO")
    entre_turno = BooleanField(default=False)
    duracion_min = IntegerField(default=30)
    duracion_real = IntegerField(null=True)
    notas = TextField(null=True)
    creado_el = DateTimeField(default=datetime.datetime.now)
    actualizado_el = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "turnos"
