from enum import Enum, IntEnum, auto


class MaybeBoolean(Enum):
    FALSE = 1

    # MAYBE = 2

    # Voor dingen die niet geautomatiseerd kunnen worden (bijv. placeholder criteria)
    CANNOT_BE_AUTOMATED = 3

    # Voor als evaluatie later nog eens geprobeerd moet worden (bijv. mozaiekregels waar nog
    # onvoldoende omliggende vlakken een habitattype hebben)
    POSTPONE = 4

    TRUE = 5

    def __invert__(self):
        if self == MaybeBoolean.TRUE:
            return MaybeBoolean.FALSE
        elif self == MaybeBoolean.FALSE:
            return MaybeBoolean.TRUE
        else:
            return self

    def __bool__(self):
        raise RuntimeError("Cannot convert MaybeBoolean to bool")

    def __and__(self, other):
        and_order = {
            MaybeBoolean.FALSE: 1,
            MaybeBoolean.POSTPONE: 2,
            MaybeBoolean.CANNOT_BE_AUTOMATED: 3,
            MaybeBoolean.TRUE: 4,
        }
        and_resolver = {v: k for k, v in and_order.items()}
        if not isinstance(other, MaybeBoolean):
            return NotImplemented
        return and_resolver[min(and_order[self], and_order[other])]

    def __or__(self, other):
        or_order = {
            MaybeBoolean.FALSE: 1,
            MaybeBoolean.CANNOT_BE_AUTOMATED: 2,
            MaybeBoolean.POSTPONE: 3,
            MaybeBoolean.TRUE: 4,
        }
        or_resolver = {v: k for k, v in or_order.items()}
        if not isinstance(other, MaybeBoolean):
            return NotImplemented
        return or_resolver[max(or_order[self], or_order[other])]

    def __str__(self):
        return self.name


class Kwaliteit(Enum):
    NVT = "Nvt"  # bijvoorbeeld in het geval van H0000 en HXXXX
    # NOTE: Ik heb dit weggehaald want ik ben NVT en ONBEKEND door mekaar wezen halen, en eigenlijk past NVT ook wel bij HXXXX
    # ONBEKEND = "Onbekend"  # bijvoorbeeld in het geval van HXXXX
    GOED = "Goed"
    MATIG = "Matig"

    @classmethod
    def from_letter(cls, letter: str) -> "Kwaliteit":
        if letter == "G":
            return cls.GOED
        elif letter == "M":
            return cls.MATIG
        else:
            raise ValueError("Letter moet G of M zijn")

    def as_letter(self) -> str:
        if self == Kwaliteit.GOED:
            return "G"
        elif self == Kwaliteit.MATIG:
            return "M"
        elif self in [Kwaliteit.NVT]:
            return "X"
        else:
            raise ValueError("GoedMatig is niet Goed of Matig")


class MatchLevel(IntEnum):
    """
    Enum voor de match levels van VvN en SBB
    """

    NO_MATCH = 0
    KLASSE_VVN = 1
    KLASSE_SBB = 2
    ORDE_VVN = 3
    VERBOND_VVN = 4
    VERBOND_SBB = 5
    ASSOCIATIE_VVN = 6
    ASSOCIATIE_SBB = 7
    SUBASSOCIATIE_VVN = 8
    SUBASSOCIATIE_SBB = 9
    GEMEENSCHAP_VVN = 10
    GEMEENSCHAP_SBB = 11


class KeuzeStatus(Enum):
    # 1 Habitatvoorstel met kloppende mits
    DUIDELIJK = auto()

    # Geen habitatvoorstel met kloppende mits
    GEEN_KLOPPENDE_MITSEN = auto()

    # Vegtypen niet in deftabel gevonden
    VEGTYPEN_NIET_IN_DEFTABEL = auto()

    # Vlak heeft uit de kartering geen vegetatietypen
    GEEN_OPGEGEVEN_VEGTYPEN = auto()

    # Meerdere even specifieke habitatvoorstellen met kloppende mitsen
    MEERDERE_KLOPPENDE_MITSEN = auto()

    # Er zijn PlaceholderCriteriums, dus handmatige controle
    PLACEHOLDER = auto()

    # # Dit gaat Veg2Hab niet op kunnen lossen
    # HANDMATIGE_CONTROLE = auto()

    # Er is meer dan threshold % HXXXX in de omliggende vlakken
    WACHTEN_OP_MOZAIEK = auto()

    def toelichting(self):
        if self == KeuzeStatus.DUIDELIJK:
            return "Als alle regels gevolgd worden is er 1 duidelijke optie; er is maar 1 habitatvoorstel met kloppende mits/mozaiek."
        elif self == KeuzeStatus.GEEN_KLOPPENDE_MITSEN:
            return "Er is geen habitatvoorstel met kloppende mits/mozaiek. Er kan dus geen habitattype toegekend worden."
        elif self == KeuzeStatus.VEGTYPEN_NIET_IN_DEFTABEL:
            return "De vegetatietypen van het vlak zijn niet in de definitietabel gevonden en leiden dus niet tot een habitattype."
        elif self == KeuzeStatus.GEEN_OPGEGEVEN_VEGTYPEN:
            return "Er zijn in de vegetatiekartering geen (habitatwaardige)vegetatietypen opgegeven voor dit vlak. Er is dus geen habitattype toe te kennen."
        elif self == KeuzeStatus.MEERDERE_KLOPPENDE_MITSEN:
            return "Er zijn meerdere habitatvoorstellen met kloppende mits/mozaiek. Er is geen duidelijke keuze te maken."
        elif self == KeuzeStatus.PLACEHOLDER:
            return "Er zijn placeholder mitsen/mozaiekregels gevonden; deze kunnen (nog) niet door Veg2Hab worden gecontroleerd."
        # elif self == KeuzeStatus.HANDMATIGE_CONTROLE:
        #     assert (
        #         False
        #     ), "Bij KeuzeStatus.HANDMATIGE_CONTROLE moet nog een mooie toelichting, maar ik weet nu nog niet hoe of wat precies, want deze KeuzeStatus is nog niet in gebruik."
        elif self == KeuzeStatus.WACHTEN_OP_MOZAIEK:
            return "Er is te weinig informatie over de habitattypen van omliggende vlakken (teveel HXXXX)"


class FGRType(Enum):
    DU = "Duinen"
    GG = "Getijdengebied"
    HL = "Heuvelland"
    HZ = "Hogere Zandgronden"
    LV = "Laagveengebied"
    NI = "Niet indeelbaar"
    RI = "Rivierengebied"
    ZK = "Zeekleigebied"
    AZ = "Afgesloten Zeearmen"
    NZ = "Noordzee"
