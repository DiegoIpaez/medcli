import datetime

from peewee import (
    AutoField,
    BooleanField,
    DateField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
)

from ..utils.constantes import DURACION_TURNO_POR_DEFECTO_MIN

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

ESTADOS_TURNO = ["RESERVADO", "ATENDIDO", "CANCELADO", "AUSENTE"]


class BaseModel(Model):
    class Meta:
        database = db


class Especialidad(BaseModel):
    id = AutoField(primary_key=True)
    nombre = TextField(unique=True)
    creado_el = DateTimeField(default=datetime.datetime.now)
    actualizado_el = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "especialidades"


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
    cuil = TextField(unique=True)
    fecha_nacimiento = DateField()
    obra_social = ForeignKeyField(ObraSocial, column_name="obra_social_id", backref="pacientes", null=True)
    creado_el = DateTimeField(default=datetime.datetime.now)
    actualizado_el = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "pacientes"


class Medico(BaseModel):
    id = AutoField(primary_key=True)
    nombre = TextField()
    especialidad = ForeignKeyField(Especialidad, column_name="especialidad_id", backref="medicos")
    matricula = TextField(unique=True)
    activo = BooleanField(default=True)
    creado_el = DateTimeField(default=datetime.datetime.now)
    actualizado_el = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "medicos"


class TurnoEstado(BaseModel):
    id = AutoField(primary_key=True)
    nombre = TextField(unique=True)
    creado_el = DateTimeField(default=datetime.datetime.now)
    actualizado_el = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "turno_estados"


class Turno(BaseModel):
    id = AutoField(primary_key=True)
    paciente = ForeignKeyField(Paciente, column_name="paciente_id", backref="turnos")
    medico = ForeignKeyField(Medico, column_name="medico_id", backref="turnos")
    fecha = DateField()
    horario = TextField()
    estado = ForeignKeyField(TurnoEstado, column_name="estado_id", backref="turnos")
    entre_turno = BooleanField(default=False)
    duracion_min = IntegerField(default=DURACION_TURNO_POR_DEFECTO_MIN)
    duracion_real = IntegerField(null=True)
    notas = TextField(null=True)
    creado_el = DateTimeField(default=datetime.datetime.now)
    actualizado_el = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "turnos"
